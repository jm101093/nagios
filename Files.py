import os
import datetime
import socket
import time
import datetime
import glob

#directory = os.listdir("/Users/jklre/nagios")
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
        timeCompare(currentTime, createTime, item)
    done(i)

def timeCompare(currentTime, createTime, item):
    timeDif = createTime + 3600
    if currentTime >= timeDif:
        HoursOld = createTime / 3600
        printTime= time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(createTime))
        print "1 CRIT", "file", item, "is", HoursOld, "Hours Old"
    else: print("0 OK file", item, "is", printTime, "old")
    print " "

def done (i):
    print "filecount =" , i

path = '.'

for root, dirs, files in os.walk(path, topdown=True):
    for name in files:
        fileName = os.path.join(root, name)
        print("Filename: " + fileName)
        fileStats = os.stat(fileName)
        print("     Protection Bits: " + str(fileStats.st_mode))
        print("     Last Changed: " + time.strftime("%Z - %Y/%m/%d, %H:%M:%S", time.localtime(fileStats.st_ctime)))
    # for name in dirs:
    #     print(os.path.join(root, name))

# for root, dirs, files in os.walk(path):
#     # do whatever you want to with dirs and files
#     if root != path:
#         # one level down, modify dirs in place so we don't go any deeper
#         del dirs[:]

#myFiles2 = os.listdir('/')
#myFiles = os.walk('**', True, None, False)
#myPyFiles = glob.glob('**/*.*')
i =0
#countFiles(i, myPyFiles)




