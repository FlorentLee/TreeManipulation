from Bio import Phylo
from collections import deque
from TimeConversion import *
import re
import pandas as pd
import numpy as np

# tree = Phylo.read('/Users/u0150975/Downloads/Visualisation/discreteTutorialFiles/longRuns/BSSVS/mcc.treefile', 'nexus')
# df = pd.read_csv('/Users/u0150975/Downloads/Visualisation/discreteTutorialFiles/locationStates.csv')
# floatPattern = re.compile(r'(?<=\_)\d+\.?\d+')
tree = Phylo.read('/Users/u0150975/Downloads/Visualisation/B.1.619_country.tree', 'nexus')
df = pd.read_csv('/Users/u0150975/Downloads/Visualisation/locations.csv')
floatPattern = re.compile(r'(?<=\|)\d+\-?\d+\-?\d+')
quotedStringPattern = re.compile(r'\"(.*)\"')


clades = []

for clade in tree.find_clades():
    clade_info = {'visited_times': 0}

    duration = clade.branch_length
    end_name = str(clade.name)

    if end_name != 'None':
        endDate = floatPattern.findall(end_name)[0]
        endDateTime = toDateTime(endDate)
        endDateDecimal = toDateDecimal(endDateTime)
        end_time = endDateDecimal
        # end_time = float(endDate)
        start_time = end_time - duration
    else:
        start_time = 0.0
        end_time = 0.0

    clade_info['duration'] = duration
    clade_info['end_name'] = end_name
    clade_info['start_time'] = start_time
    clade_info['end_time'] = end_time

    clade_info['start_latitude'] = 0.0
    clade_info['start_longitude'] = 0.0

    details = clade.comment.split(',')
    # state = quotedStringPattern.findall(''.join([item for item in details if 'state=' in item]))[0]
    location = quotedStringPattern.findall(''.join([item for item in details if 'location=' in item]))[0]

    # end_location = np.asarray(df.loc[df['State'] == state].values)[0]
    end_location = np.asarray(df.loc[df['location'] == location].values)[0]
    end_latitude = end_location[1]
    end_longitude = end_location[2]

    clade_info['end_latitude'] = end_latitude
    clade_info['end_longitude'] = end_longitude

    clades.append(clade_info)

stack = deque()

for clade in clades:
    if not stack:
        stack.append(clade)
    while stack[-1]['visited_times'] == 2:
        temp = stack.pop()
        temp['start_latitude'] = stack[-1]['end_latitude']
        temp['start_longitude'] = stack[-1]['end_longitude']
        stack[-1]['end_time'] = temp['start_time']
        stack[-1]['start_time'] = stack[-1]['end_time'] - stack[-1]['duration']
        stack[-1]['visited_times'] += 1
    stack.append(clade)
    if stack[-1]['end_name'] != 'None':
        temp = stack.pop()
        temp['start_latitude'] = stack[-1]['end_latitude']
        temp['start_longitude'] = stack[-1]['end_longitude']
        stack[-1]['end_time'] = temp['start_time']
        stack[-1]['start_time'] = stack[-1]['end_time'] - stack[-1]['duration']
        stack[-1]['visited_times'] += 1

for clade in clades:
    clade['start_time'] = decimalToTimeStamp(clade['start_time'])
    clade['end_time'] = decimalToTimeStamp(clade['end_time'])
    if clade['start_latitude'] == 0.0 and clade['start_longitude'] == 0.0:
        clade['start_latitude'] = clade['end_latitude']
        clade['start_longitude'] = clade['end_longitude']
    del clade['visited_times']
    del clade['end_name']

df = pd.DataFrame.from_dict(clades)
# df.to_csv(r'/Users/u0150975/Downloads/Visualisation/test.csv', index=False, header=True)
df.to_csv(r'/Users/u0150975/Downloads/Visualisation/B.1.619_country.csv', index=False, header=True)

