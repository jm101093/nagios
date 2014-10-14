import os
import datetime
import socket

directory = os.listdir("c:\\nagios\\nagios")
print directory

from os import walk

#f = []
#for (dirpath, dirnames, filenames) in walk(directory):
#    f.extend(filenames)
 #   break

x=0
for item in directory:
    print(x ,".", item)
    x=x+1
    if directory == "":
        break