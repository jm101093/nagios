#!/usr/bin/python
#check_mk Nagios elastic search cluster status monitor
import requests

userid = ''
password = ''
r = requests.get('https://(youor elastic cluster)/_cluster/health?pretty=true', verify=False, auth=(userid, password))
response = r.json()
Status = response.values()[0]
Good = "green"
Ok = "yellow"
Bad = "red"

if Status == Good:
	print "0 Elastic_Cluster_pelkc2 elastic_cluster_status=green OK_GREEN"
elif Status == Ok:
	print "1 Elastic_Cluster_pelkc2 elastic_cluster_status=yellow WARN_YELLOW"
elif Status == Bad:
	print "2 Elastic_Cluster_pelkc2 elastic_cluster_status=red CRIT_RED"
else:
	print "3 Elastic_Cluster_pelkc2 elastic_cluster_status is unknown"
