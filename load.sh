#!/bin/bash

bin=$1
if [[ -z "$bin" ]]; then
    bin="./dist/"$(ls ./dist/ | grep "load-" | head -1)
fi

if [[ -z "$COUNT" ]]; then
    echo "Count required"
    exit 1
fi

if [[ -z "$MAX" ]]; then
    echo "Max required"
    exit 1
fi

if [[ -z "$URL" ]]; then
    echo "URL required"
    exit 1
fi

if [[ $(($MAX%$COUNT)) != 0 ]]; then
    echo "Wrong values"
    exit 1
fi

workers=$(($MAX/$COUNT))

min=1
max=$(($workers))

for i in `seq 1 $COUNT`; do
    URL=$URL MIN=$min MAX=$max nohup $bin </dev/null > "logs/load_$i.log" 2>&1 &
    echo "URL=$URL MIN=$min MAX=$max nohup $bin </dev/null > \"logs/load_$i.log\" 2>&1 &"
    min=$(($max+1))
    max=$(($min+$workers-1))
done

