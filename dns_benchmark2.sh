#!/bin/sh

mintime='99999999999'
mindns=''

input="$1"

while read -r DNS; do
	runtime="$(dig "@$DNS" gmail.com|grep Query | awk '{print($4)}')"
	echo "$DNS $runtime ms"
	if [ "$runtime" -le "$mintime" ]; then
		mintime="$runtime"
		mindns="$DNS"
	fi
done < "$input"

echo "Fast response: $mintime ms from $mindns"
