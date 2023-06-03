#!/usr/bin/env python
#check_mk JBoss JMSQ mnitor for Nagios check_mk

from __future__ import print_function
import sys
import os
import json
import base64
import requests

### Username should be AD login without corp, i.e. aa1111111
USERNAME = os.getenv('CICD_USER', 'USERID')

### Can make this an environment variable or put it in plain text here
PASSWORD = os.getenv('CICD_USER_PASSWORD', 'PASSWORD')

### Default cluster to query is JBC9. Can make this a parameter if you want
CLUSTER_NUMBER = int(os.getenv('CLUSTER', '9'))

### No need to touch this
PORT = 10000 + 2*CLUSTER_NUMBER

### Can touch this if needed. 
NODE_NO = os.getenv('NODE')

### You will need rights to hit the HTTP API
ENV = os.getenv('ENV', 'd')

### Max messgae threshold
CRITICAL_THRESHOLD = os.getenv('CRITICAL_THRESHOLD', 100)
WARN_THRESHOLD = os.getenv('WARN_THRESHOLD', 100)

RULES = dict()
headers = {'Authorization': 'Basic {0}'.format(base64.b64encode('{0}:{1}'.format(USERNAME, PASSWORD))), 'Content-Type': 'application/json'}
URL = 'http://{0}jbc{1}SERVERNAME:{2}/management'.format(ENV, CLUSTER_NUMBER, PORT)


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def load_rules(path='rules.json'):
    if not os.path.exists(path):
        return
    with open(path, 'r') as f:
        RULES.update(json.load(f))

def get_node_list():
    node_list = []
    data = {'operation': 'read-children-resources', 'child-type': 'host'}
    response = requests.post(url=URL, data=json.dumps(data), headers=headers)
    response.raise_for_status()
    response_data = response.json()['result']
    for host in sorted(response_data):
       if host.find('hc') > 0:
          node_no = ''.join(c for c in host.split('n')[1] if c in '1234567890')
          node_list.append(node_no)
    if len(node_list) == 0:
        eprint('ERROR: unable to determine node list.')
        exit(1)
    return node_list

def get_all_queue_stats(nodes=[1]):
    for node in nodes:
        data = {
            'address': [
                {'host': '{0}jbc{1}n{2}-hc'.format(ENV, CLUSTER_NUMBER, node)},  #host name format for jboss cluster
                {'server': 'node{0}'.format(node)},
                {'subsystem': 'messaging-activemq'},
                {'server': 'default'}
            ],
            'operation': 'read-children-resources',
            'child-type': 'jms-queue',
            'include-runtime': True
        }
        response = requests.post(url=URL, data=json.dumps(data), headers=headers)
        response.raise_for_status()
        response_data = response.json()['result']
        for queue in response_data:
            if queue in RULES:
                if response_data[queue]['message-count'] >= RULES[queue]['CRITICAL']:
                    print('2 JBC{0}_{1} message-count={2} CRITICAL - {2} messages in {4}JBC{0}N{3}_{1}'.format(CLUSTER_NUMBER, queue, response_data[queue]['message-count'], node, ENV.upper()))
                    continue
                elif response_data[queue]['message-count'] >= RULES[queue]['WARNING']:
                    print('1 JBC{0}_{1} message-count={2} WARN - {2} messages in {4}JBC{0}N{3}_{1}'.format(CLUSTER_NUMBER, queue, response_data[queue]['message-count'], node, ENV.upper()))
                    continue
                else:
                    print('0 JBC{0}_{1} message-count={2} OK - {2} messages in {4}JBC{0}N{3}_{1}'.format(CLUSTER_NUMBER, queue, response_data[queue]['message-count'], node, ENV.upper()))
                    continue
            elif response_data[queue]['message-count'] > CRITICAL_THRESHOLD:
                print('2 JBC{0}_{1} message-count={2} CRITICAL - {2} messages in {4}JBC{0}N{3}_{1}'.format(CLUSTER_NUMBER, queue, response_data[queue]['message-count'], node, ENV.upper()))
                continue
            elif response_data[queue]['message-count'] > WARN_THRESHOLD:
                print('1 JBC{0}_{1} message-count={2} WARN - {2} messages in {4}JBC{0}N{3}_{1}'.format(CLUSTER_NUMBER, queue, response_data[queue]['message-count'], node, ENV.upper()))
                continue
            else:
                print('0 JBC{0}_{1} message-count={2} OK - {2} messages in {4}JBC{0}N{3}_{1}'.format(CLUSTER_NUMBER, queue, response_data[queue]['message-count'], node, ENV.upper()))
                continue


if NODE_NO is None:
   NODE_LIST = get_node_list()
else:
   NODE_LIST = [NODE_NO]
load_rules()
get_all_queue_stats(NODE_LIST)


"""
Sample JSON response for queue info:

{
    "outcome": "success",
    "result": {
        "consumer-count": 4,
        "dead-letter-address": "jms.queue.CORE_SERVICES.MESSAGE_BUS_REJECT_Q",
        "delivering-count": 0,
        "durable": true,
        "entries": [
            "java:jboss/exported/jms/queue/CORE_SERVICES.MESSAGE_BUS_Q"
        ],
        "expiry-address": "jms.queue.CORE_SERVICES.MESSAGE_BUS_REJECT_Q",
        "legacy-entries": null,
        "message-count": 0,
        "messages-added": 651,
        "paused": false,
        "queue-address": "jms.queue.CORE_SERVICES.MESSAGE_BUS_Q",
        "scheduled-count": 0,
        "selector": null,
        "temporary": false
    }
}
"""
