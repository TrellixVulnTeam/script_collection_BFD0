#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 09:35:32 2021
@author: benmulcahy

Made to plot UNC-49::RFP puncta along body of worms as they progress through development
The path should be a folder containing the csv files generated from FIJI's 'Plot Profile' function
Basically max intensity projections were made of confocal stacks of UNC-49::RFP worms. The stacks were preprocessed with gaussian blur(sigma = 2), subtract background (rolling ball = 50px). Draw a segmented line over ventral cord, plot profile, save data as csv. Do same for dorsal. 
Make sure ventral and dorsal csvs have 'ventral and 'dorsal' in title, respectively, as that's how they are seperated below

Change the path, n_bins, and group_name as necessary

"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

path = "/Users/benmulcahy/Dropbox/data/DD_VD_remodeling/UNC-49_quantification/1h/" #folder containing csv files
n_bins = 50 # number of bins to use along body axis
group_name = '1h' # for plot title

# get list of files in folder
filelist = []
for file in os.listdir(path):
    filelist.append(path + file)
    
temp_dfs = []
index = 1 # to add replicate column
body_pos = list(range(0, n_bins)) # to be appended to binned dataframe later
for f in filelist:
    if 'csv' not in f:
        continue
    df_temp = pd.read_csv(f)
    df_temp.columns = ['body_position', 'intensity']
    intensity = df_temp['intensity']
    length = len(intensity)
    interval = int(length / n_bins) # find intervals to resample to the number of bins specifiec by n_bins
    binned_intensity = []
    for x in range (n_bins): # do the resampling
        start = interval * x
        end = start + interval
        mean_bin = np.mean(intensity[start:end])
        binned_intensity.append(mean_bin)
    if 'ventral' in f:
        side = ['ventral'] * n_bins
    else:
        side = ['dorsal'] * n_bins
    df_binned = pd.DataFrame( 
                             {'body_pos': body_pos,
                              'intensity': binned_intensity,
                              'replicate': index,
                              'side': side
                              })
    temp_dfs.append(df_binned)
    index = index + 1
    
df = pd.concat(temp_dfs, ignore_index=True)    


# plot intensity over body length
sns.lineplot(data=df, x='body_pos', y='intensity', hue='side', hue_order= ['ventral', 'dorsal'], palette = ['r', 'b'])
plt.title(group_name)
plt.ylim(0,600)


