#!/bin/bash
#check_mk local check for memstat metrics in AIX

Memcheck=`/usr/local/bin/memstat.ksh`

CRIT=3072
WARN=3000

read -a arr <<<$Memcheck

ALERT=${arr[1]%%.*}

if [[ $ALERT -le $CRIT ]]; then 
    echo "2"" ""MemoryStat_FreeMemory" "FreeMemory=""${arr[1]}"" ""Freememory="" ""${arr[1]}" " "" FreeMem"
elif [[ $ALERT -le $WARN ]]; then
   	echo "1"" ""MemoryStat_FreeMemory" "FreeMemory=""${arr[1]}"" ""Freememory="" ""${arr[1]}" " "" FreeMem"
else echo "0"" ""MemoryStat_FreeMemory" "FreeMemory=""${arr[1]}"" ""Freememory="" ""${arr[1]}" " "" FreeMem"
fi

echo "0"" ""MemoryStat_FileSystemCache" "FileSystemCache=""${arr[0]}"" ""FileSystemCache="" ""${arr[0]}" " "" FileCache"
