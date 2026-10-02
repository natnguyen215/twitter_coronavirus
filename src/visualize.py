#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_path',required=True)
parser.add_argument('--key',required=True)
parser.add_argument('--percent',action='store_true')
args = parser.parse_args()

# imports
import os
import json
from collections import Counter,defaultdict

# open the input path
with open(args.input_path) as f:
    counts = json.load(f)

# normalize the counts by the total values
if args.percent:
    for k in counts[args.key]:
        counts[args.key][k] /= counts['_all'][k]

# print the count values
items = sorted(counts[args.key].items(), key=lambda item: (item[1],item[0]), reverse=True)
for k,v in items:
    print(k,':',v)

# visualize
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# get top 10 items
top_items = items[:10]

# sort from low to high
top_items_sorted = sorted(top_items, key=lambda item: (item[1], item[0]), reverse=False)

# extract labels and values
labels = [k for k, v in top_items_sorted]
values = [v for k, v in top_items_sorted]

# determine axis label based on input path
if args.input_path.endswith('.country'):
    x_label = 'country'
else:
    x_label = 'language'

# create bar graph
plt.figure(figsize=(10, 6))
plt.bar(range(len(labels)), values)
plt.xticks(range(len(labels)), labels, rotation=45, ha='right')
plt.xlabel(x_label)
plt.ylabel('count')
plt.title(f'{args.key if args.key.isascii() else "#coronavirus (Korean)"} by {x_label}')

# save the plot as png
# derive filename from input path and key
input_basename = os.path.basename(args.input_path)
key_sanitized = args.key.replace('#', '')
output_filename = f"{input_basename}_{key_sanitized}.png"

plt.savefig(output_filename)
plt.close()

