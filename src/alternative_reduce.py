#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--hashtags', nargs='+', required=True)
args = parser.parse_args()

# imports
import os
import json
import glob
import datetime

# initialize counts
days = []
counts = {hashtag: [] for hashtag in args.hashtags}

# load each mapper output
paths = sorted(glob.glob('outputs/geoTwitter20-*.lang'))
for path in paths:
    filename = os.path.basename(path)
    date = datetime.datetime.strptime(filename, 'geoTwitter%y-%m-%d.zip.lang')
    days.append(date.timetuple().tm_yday)

    with open(path) as f:
        daily_counts = json.load(f)

    for hashtag in args.hashtags:
        counts[hashtag].append(sum(daily_counts.get(hashtag, {}).values()))

# visualize
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

for hashtag in args.hashtags:
    plt.plot(days, counts[hashtag], label=hashtag)

plt.xlabel('day of year')
plt.ylabel('number of tweets')
plt.title('hashtag usage during 2020')
plt.legend()
plt.tight_layout()
plt.savefig('alternative_reduce.png')
plt.close()

