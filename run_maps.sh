#!/bin/sh
mkdir -p logs
for file in '/data/Twitter dataset/'geoTwitter20-*.zip; do
    nohup python3 ./src/map.py --input_path="$file" &
done
