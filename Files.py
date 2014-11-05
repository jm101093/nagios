import os
import datetime
import socket
import time
import datetime
import glob

directory = os.listdir("c:\\nagios\\nagios")
#print directory
from os import walk

#f = []
#for (dirpath, dirnames, filenames) in walk(directory):
#    f.extend(filenames)
 #   break

def countFiles (i, myPyfiles):
    for item in myPyFiles:
        i = i+1
        currentTime = int(time.time())
        createTime = os.path.getctime(item)
        #sortedFiles = createTime.sort(key=os.path.getctime)
        timeDays = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(createTime))
        date_time = timeDays
        pattern = '%Y-%m-%d %H:%M:%S'
        epoch = int(time.mktime(time.strptime(date_time, pattern)))
        print item
        print(timeDays)
        print "Epoch =", epoch
        print "The Time is", currentTime
        print " "
    done(i)

def timeCompare(currentTime, createTime):

    if currentTime ==


def done (i):
    print "filecount =" , i

#x=0
#for item in directory:
#    print x ,".", item
#    x = x + 1
#    if directory == "":
#        break

myPyFiles = glob.glob('c:/windows/system32/*.dll')
i =0
countFiles(i, myPyFiles)




