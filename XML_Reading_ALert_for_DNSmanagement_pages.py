#!/bin/python
#XML data parser for DNS Devices.  Nagios check_mk locak check
import urllib2
import xml
import xml.etree.ElementTree as et
import os

file = urllib2.urlopen('URL_GOES_HERE')
data = file.read()
file.close()

parseData = xml.etree.ElementTree.fromstring(data)
xml_data2 = parseData.findall("bind/statistics/socketmgr")

for x in xml_data2:
	name2 = x.findall("sockets/socket/name")
	localaddress = x.findall("sockets/socket/local-address")
	Type = x.findall("sockets/socket/type")
	states = x.findall("sockets/socket/states/state")

j = 0

while j < len(name2):
	name = name2[j].text + str(j)
	print "0 ", name, "- OK", localaddress[j].text,name2[j].text, Type[j].text, states[j].text, "If I do not appear in the list. Priority 2."
	j = j+1
