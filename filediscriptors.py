#!/usr/bin/env python
#IO file thingie monitor for *nix file descriptor monitoring  Check_mk nagios local check by Jeremy Mclaurin
#jklre2001@yahoo.com
import commands
outputFilebeat = commands.getoutput('cat /proc/sys/fs/file-nr');

a,b,c = outputFilebeat.split();

filedescriptors = int(c) - int(b);
threshold1 = 0.8*filedescriptors;
threshold2 = 0.7*filedescriptors;


if threshold2 > b:
    print('2 FileDescriptors FileDescriptors=%s CRIT FileDescriptors=%s' % (b, b));
elif threshold1 > b:
    print('1 FileDescriptors FileDescriptors=%s WARN FileDescriptors=%s' % (b, b));
else:
	print('0 FileDescriptors FileDescriptors=%s OK FileDescriptors=%s' % (b, b));
