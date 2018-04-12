#!/bin/bash

declare -a dnstime

mintime=99999999999
mindns=""
for DNS in $(cat $1)
do

runtime=$(dig @$DNS gmail.com|grep Query | awk '{print($4)}')
echo $DNS $runtime ms
if [ "$runtime" -le "$mintime" ]; then

 mintime=$runtime
 mindns=$DNS
fi
done


echo "Fast response: $mintime ms from $mindns"


