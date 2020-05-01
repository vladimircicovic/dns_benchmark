#!/bin/bash

declare -a dnstime

mintime=99999999999
mindns=""
for DNS in $(cat $1)
do
start=$(($(date +%s%N)/1000000))
nslookup github.com $DNS >> /dev/null
end=$(($(date +%s%N)/1000000))

runtime=$((end-start ))
echo $DNS $runtime ms
if [ "$runtime" -le "$mintime" ]; then

 mintime=$runtime
 mindns=$DNS
fi
done


echo "Fast response: $mintime from $mindns"


