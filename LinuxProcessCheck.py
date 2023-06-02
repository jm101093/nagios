#!/usr/bin/env python
#process monitor
#replace filebeats with your service name
import commands
outputCommand = commands.getoutput('ps -ef | grep filebeats |grep -v grep')

Lines = len(str.splitlines(outputCommand))

if Lines == 1:
    print("0 filebeats filebeats_service=running OK filebeats_is_up_and_running!")
elif Lines == 0:
	print("2 filebeats filebeats_service=Stopped CRIT filebeats_is_not_running!")
else :
	print("3 Filebeats filebeats_service=Stopped UNKW UNKN_filebeats_is_not_running!")
