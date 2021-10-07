# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 14:48:05 2020
Generates a csv file containing paths to images, with x, y and z coordinates for
import into TrakEM2. x and y are always 0 (TrakEM2 can figure it out later),
and z is the z layer for each section.

The input files must be named as the following:
GXX_SXX.tif, where X is a number (e.g. G01_S01.tif)

@author: Ben Mulcahy
"""

import os
import re
import pandas as pd

path = "D:/EM18-138_series/EM18-138_unstained_series/raw_images"

# make list of tiles
file_list = []
for f in os.listdir(path):
    file_list.append(f)

# make list without overview images
file_list_minus_overview = []
for f in file_list:
    if "overview" in f:
        continue
    file_list_minus_overview.append(f)

# make list of sections
section_list = []
for f in file_list_minus_overview:
    section = re.search('(G.*)_0', f)
    section_list.append(section.group(1))

# list of unique sections
short_section_list = sorted(list(set(section_list)))
n_sections = len(short_section_list)

# generate z coordinates
z_num = []
for s in section_list:
    for s1 in short_section_list:
        if s == s1:
            z_num.append(short_section_list.index(s1))

# generate path list
pathlist = []
for s in file_list_minus_overview:
    pathlist.append(path + "/" + s)

xpos = []
ypos = []
for s in file_list_minus_overview:
    xpos.append(0)
    ypos.append(0)

# merge into dataframe
df = pd.DataFrame({
                'path': pathlist,
                'xpos': xpos,
                'ypos': ypos,
                'zpos': z_num
                })

# write to csv
out_name = path + "/" + "tile_coordinates.csv"
df.to_csv(out_name, index=False, header=False)
