#!/usr/bin/env python
#crappy script monitor by Jeremy Mclaurin
#jklre2001@yahoo.com
import re
import subprocess
import commands
import time

output = commands.getoutput('service nagios status');
regex = 'nagios.\(pid \d+\).is.running...'
regex2 = 'Starting nagios: done.'
pattern = re.compile(regex)
pattern1 = re.compile(regex2)
results = re.findall(pattern,output)

if len(results) > 0:
	print("OK")
	var = commands.getoutput('mail -s "Nagios Service OK" jeremy.mclaurin@mitchell.com < /dev/null')
else:
	correct = commands.getoutput('service nagios start');
	time.sleep(5)
	corrector = re.findall(pattern1,correct)
	if len(corrector) > 0:
		var = commands.getoutput('mail -s "Nagios Service Started" jeremy.mclaurin@mitchell.com < /dev/null')
	else:
		var2 = commands.getoutput('mail -s "Nagios Service in trouble" jeremy.mclaurin@mitchell.com < /dev/null')