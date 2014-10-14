import os
import datetime
import socket
import glob

directory = os.listdir("c:\\nagios\\nagios")
print directory

from os import walk

#f = []
#for (dirpath, dirnames, filenames) in walk(directory):
#    f.extend(filenames)
 #   break

def countFiles (i, myPyfiles):
    for item in myPyFiles:
        i = i+1
    #return i
    done(i)

def done (i):
    print('filecount=',(i))

x=0
for item in directory:
    print(x ,".", item)
    x=x+1
    if directory == "":
        break

myPyFiles = glob.glob('c:/windows/system32/*.dll')
i =0
countFiles(i, myPyFiles)




