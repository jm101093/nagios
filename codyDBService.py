#!/usr/bin/env python
import pymssql

server = ""
user =""
password = ""

conn = pymssql.connect(host=server, user=user, password=password, database='databasename', as_dict=False)
print "connecting"
cursor = conn.cursor()
print "next"

cursor.execute("EXEC msdb.dbo.sysmail_help_status_sp;")

print cursor.fetchone()

result = cursor.fetchone()

if result == 0:
	print "0 status OK"
if result == 1:
	print "1 status critical"

conn.close()



#IF (@MsgWaiting > @MaxMsgWaiting) 
#       PRINT N'ERROR -- PENDING OUTBOUND MESSAGE.  There are '+CAST(@MsgWaiting as nvarchar)+N' Messages waiting to be sent *** System: ' + @@Servername + ':' + DB_NAME()
#ELSE
#       PRINT 'NO pending outbound messages *** System: ' + @@Servername + ':' + DB_NAME()
