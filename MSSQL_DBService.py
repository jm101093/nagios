#!/usr/bin/env python
#nagios check_mk MSSQL monitor
#MSSQL monitor.  Replace with whatever query server user creds and databasename to whatever you want and thresholds
import pymssql

server = "Servername"
user ="User_ID"
password = "Password"

conn = pymssql.connect(host=server, user=user, password=password, database='DatabaseName', as_dict=False)
print "connecting"
cursor = conn.cursor()
print "next"

cursor.execute("""Declare @OutBID int, @LastPID int, @MsgWaiting int, @MaxMsgWaiting int;
SET @MaxMsgWaiting = 50;
SET @OutBID = 0;
SET @LastPID = 0;

SELECT @OutBID = max(OutboundMessageID) 
FROM   OutboundMessage 

SELECT @LastPID = LastProcessedID 
FROM ExternalTaskRun 
WHERE ExternalTaskID=6 AND ExternalTaskRunID=1

SET @MsgWaiting = @OutBID - @LastPID

IF (@MsgWaiting > @MaxMsgWaiting) 
SELECT N'ERROR -- PENDING OUTBOUND MESSAGE.  There are '+CAST(@MsgWaiting as nvarchar)+N' Messages waiting to be sent *** System: ' + @@Servername + ':' + DB_NAME() AS Result
ELSE
SELECT 'NO pending outbound messages *** System: ' + @@Servername + ':' + DB_NAME() AS Result
""")

print cursor.fetchone()

result = cursor.fetchone()

if result == 0:
	print "0 status OK"
if result == 1:
	print "1 status critical"

conn.close()
