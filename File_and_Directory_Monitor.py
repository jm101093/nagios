#!/usr/bin/env python
#needs a csv file in the following format to read
#Status,Start Time,End Time,Directory Path,Monitor Name,File Name/Extension,Subdirectories Check,FileCount Threshold,OldFileAge Threshold,NewFileAge Threshold
# E,02:00,22:00,\\NetworkPath\,"regex file name match(like .zip),n,-,60,-
import os, time, stat, sys, csv
from glob import glob
from itertools import chain
import optparse, datetime, re

parser = optparse.OptionParser()
parser.add_option("-C", "--csvpath",
                     help="CSV File Path")
options, args = parser.parse_args()


def file_check(directory , file, subdirectories, fcount, firstage, lastage, monitor):
	if not directory:
		directory = r"{0}".format(os.path.dirname(os.path.realpath(__file__)))
	pattern = r"'{0}'".format(file)
	count = 0
	age1 = 0
	age2 = sys.maxint
	filename = []
	condition = 0
	fcountdisp = 0
	firstagedisp = 0
	lastagedisp = 0

	def get_stats(count, path, y, age1, age2):
		count = count + 1
		y = os.path.join(path, y)
		st = os.stat(y)
		ctime = st.st_ctime
		if int((time.time()-ctime)/60) > age1:
			age1 = int((time.time()-ctime)/60)
		if int((time.time()-ctime)/60) < age2:
			age2 = int((time.time()-ctime)/60)
		return (count, age1, age2)

	directory_name = directory.replace('\\n',"\\N")
	directory_name = directory_name.replace('\\',"\\\\",1)
	try:
		for i in os.walk(directory):
			filename.append(i)	
		if len(filename) != 0:
			if subdirectories == 'y':
				for (path,dirnames,filenames) in os.walk(directory):
					for y in filenames:
						if file == '-':
							(count, age1, age2) = get_stats(count, path, y, age1, age2)
						elif re.search(file,y) != None:
							(count, age1, age2) = get_stats(count, path, y, age1, age2)
			elif subdirectories == 'n':
				for f in os.listdir(directory):
					if os.path.isfile(os.path.join(directory,f)):
						if file == '-':
							(count, age1, age2) = get_stats(count, directory, f, age1, age2)
						elif re.search(file,f) != None:
							(count, age1, age2) = get_stats(count, directory, f, age1, age2)
			
			if count != 0:
				if fcount != '-' and count > int(fcount):
					condition = 2
				elif firstage != '-' and age1 > int(firstage):
					condition = 2
				elif lastage != '-' and age2 > int(lastage):
					condition = 2
				if fcount != '-':
					print str(condition) + " " + str(monitor) + " FileCount=" + str(count) + ";" + str(fcount) + ";" + str(fcount),
					sys.stdout.softspace = False
				elif fcount == '-':
					print str(condition) + " " + str(monitor) + " FileCount=" + str(count),
					sys.stdout.softspace = False
				if firstage != '-':
					print "|OldFileAge=" + str(age1) + ";" + str(firstage) + ";" + str(firstage),
					sys.stdout.softspace = False
				elif firstage == '-':
					print "|OldFileAge=" + str(age1),
					sys.stdout.softspace = False
				if lastage != '-':
					print "|NewFileAge=" + str(age2) + ";" + str(lastage) + ";" + str(lastage) + " ",
				elif lastage == '-':
					print "|NewFileAge=" + str(age2) + " ",

				if fcount != '-':
					if count > int(fcount):
						print "CRITICAL" + "- File Count = " + str(count) + " : ",
					else:
						print "OK" + "- File Count = " + str(count) + " : ",
				else:
					print "OK" + "- File Count = " + str(count) + " : ",

				if firstage != '-':
					if age1 > int(firstage):
						print "CRITICAL" + "- Old File Age = " + str(age1) + " Minutes : ",
					else:
						print "OK" + "- Old File Age = " + str(age1) + " Minutes : ",
				else:
					print "OK" + "- Old File Age = " + str(age1) + " Minutes : ",

				if lastage != '-':
					if age2 > int(lastage):
						print "CRITICAL" + "- New File Age = " + str(age2) + " Minutes : ",
					else:
						print "OK" + "- New File Age = " + str(age2) + " Minutes : ",
				else:
					print "OK" + "- New File Age = " + str(age2) + " Minutes : ",
				print "Directory Path = " + directory_name + " : File Name Match = " + file

			else:
				if fcount != '-':
					print str(condition) + " " + str(monitor) + " FileCount=0" + ";" + str(fcount) + ";" + str(fcount),
					sys.stdout.softspace = False
				elif fcount == '-':
					print str(condition) + " " + str(monitor) + " FileCount=0",
					sys.stdout.softspace = False
				if firstage != '-':
					print "|OldFileAge=0" + ";" + str(firstage) + ";" + str(firstage),
					sys.stdout.softspace = False
				elif firstage == '-':
					print "|OldFileAge=0",
					sys.stdout.softspace = False
				if lastage != '-':
					print "|NewFileAge=0" + ";" + str(lastage) + ";" + str(lastage) + " ",
				elif lastage == '-':
					print "|NewFileAge=0" + " ",
				print "OK" + "- File Count = 0 : ",
				print "OK" + "- Old File Age = 0 Minutes : ",
				print "OK" + "- New File Age = 0 Minutes : ",
				print "Directory Path = " + directory_name + " : File Name Match = " + file
		else:
			print "2 " + str(monitor) + " FileCount=0|OldFileAge=0|NewFileAge=0 CRITICAL- Directory Not Accessible : Directory Path = " + directory_name + " : File Name Match = " + file
	except: 
		print "2 " + str(monitor) + " FileCount=0|OldFileAge=0|NewFileAge=0 CRITICAL- Directory Not Accessible : Directory Path = " + directory_name + " : File Name Match = " + file


def main():
	with open(options.csvpath) as f:
		reader = csv.DictReader(f)
		data = [r for r in reader]

	for row in data:
		now = datetime.datetime.now()
		if row['Status'] == 'E' and now.strftime("%H:%M") > row['Start Time'] and now.strftime("%H:%M") < row['End Time']:
			file_check(row['Directory Path'], row['File Name/Extension'], row['Subdirectories Check'], row['FileCount Threshold'], row['OldFileAge Threshold'], row['NewFileAge Threshold'], row['Monitor Name'])
		elif row['Status'] == 'E' and (now.strftime("%H:%M") < row['Start Time'] or now.strftime("%H:%M") > row['End Time']):
			directory_name = row['Directory Path'].replace('\\n',"\\N")
			directory_name = directory_name.replace('\\',"\\\\",1)
			print "0 " + row['Monitor Name'] + " FileCount=0|OldFileAge=0|NewFileAge=0 OK- Monitor Disabled By Schedule : Directory Path = " + directory_name + " : File Name Match = " + row['File Name/Extension']
		elif row['Status'] == 'D':
			directory_name = row['Directory Path'].replace('\\n',"\\N")
			directory_name = directory_name.replace('\\',"\\\\",1)
			print "0 " + row['Monitor Name'] + " FileCount=0|OldFileAge=0|NewFileAge=0 OK- Monitor Disabled : Directory Path = " + directory_name + " : File Name Match = " + row['File Name/Extension']

if __name__ == "__main__":
	main()
