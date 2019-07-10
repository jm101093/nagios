#!/bin/bash

latestalerttime=$(curl -s -XGET 'localhost:9200/nagioslogserver_log/_search?q=type:alert' -d '{
  "query": {
    "match_all": {}
  },
  "size": 1,
  "sort": [
    {
      "created": {
        "order": "desc"
      }
    }
  ]
}' | cut -d":" -f17 | cut -d"," -f1 | cut -c 1-10)

currenttime=$(date +%s)

#echo $latestalerttime
#echo $currenttime

#diff current time vs last alert runtime
diff=$(($currenttime - $latestalerttime))
#echo $diff
#echo '<<nagios Log Server Jobs>>'
if [ $diff -gt 300 ]; then
        echo "2" " " "NagiosLogServerJobs" "Freshness=$diff" "All Jobs are Not Happy Freshness=$diff" 
else
        echo "0" " " "NagiosLogServerJobs" "Freshness=$diff" "All Jobs are Happy Freshness=$diff" 
fi
