# imports
import numpy as np
import pandas as pd
from datetime import datetime
import collections
from datetime import time
import random
import math
from pprint import pprint
import matplotlib.cm as cm


raw_data = pd.read_csv("turndata0627.txt")

# the below is a warning about changing values in a DF. I want to change values. I don't listen to the warnings
pd.options.mode.chained_assignment = None   


#initial data cleaning to eliminate turnstile default vals  
def clean_data(inp):
    data = inp.copy(deep="True")
    data['ENTRIES2'] = 0
    
    # remove 
    for i in range(1, len(data)):
        
        if data['SCP'][i] == data['SCP'][i-1]:
            data['ENTRIES2'][i] = data['ENTRIES'][i] - data['ENTRIES'][i-1]
    
    for i in range(0, len(data)):
        # fix values that are too high or too low                                                               
        if data['ENTRIES2'][i] > 5000:
            data['ENTRIES2'][i] = 0 # try this instead of plain old zero
        if data['ENTRIES2'][i] < 0:
            data['ENTRIES2'][i] = 0
    
    # overwrite original ENTRIES data because it's not useful
    data['ENTRIES'] = data['ENTRIES2']
    return data.copy(deep="True")

df = clean_data(raw_data)


raw_data0620 = pd.read_csv("turndata0620.txt", low_memory=False) 
raw_data0613 = pd.read_csv("turndata0613.txt", low_memory=False)
raw_data0606 = pd.read_csv("turndata0606.txt", low_memory=False)

week1 = clean_data(raw_data0620) 
week2 = clean_data(raw_data0613)
week3 = clean_data(raw_data0606)

file_list = []
total_df = None
file_list.append(df)
file_list.append(week1)
file_list.append(week2)
file_list.append(week3)
total_df = pd.concat(file_list)

time_bin_avg = {}

for i in range(len(total_df)):
    
    key = str(total_df['TIME'][i])
    val = total_df['ENTRIES'][i]
    
    if key in time_bin_avg:
        time_bin_avg[key].append(val)
    else:
        time_bin_avg[key] = [val]
        
pprint(time_bin_avg)
