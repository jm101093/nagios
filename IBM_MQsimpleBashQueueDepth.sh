#!/bin/bash
#check_mk nagios data formatter for IBMMQ to a check_mk local check

/usr/local/bin/qwatcher_pcpm.pl -m ECSTEST| awk -F'\t' -v WARN=$WARN -v CRIT=$CRIT  '(match($2, /[0123456789]+/)) {
            WARN=4; 
            CRIT=10;
            iperc= int(substr($2, RSTART, RLENGTH)); 
            if (iperc < WARN ) 
                    print "0 check_mqQueDepthTEST:"$1" QueueDeapth="$2";"WARN";"CRIT"; OK - QueueDeapth:"$2" - ChannelName:"$1;
            else if (iperc >= WARN && iperc < CRIT)
                    {print "2 check_mqQueDepthTEST:"$1" QueueDeapth="$2";"WARN";"CRIT"; WARNING - QueueDeapth:"$2" - ChannelName:"$1;}
            else if (iperc >= CRIT)
                     {print "2 check_mqQueDepthTEST:"$1" QueueDeapth="$2";"WARN";"CRIT"; CRITICAL - QueueDeapth:"$2" - ChannelName:"$1;}
}'
