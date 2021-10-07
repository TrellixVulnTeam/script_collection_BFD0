# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 10:14:40 2021

@author: mulcahy
"""

import os
import pandas as pd

in_dir = 'D:/Liver/image_sequence/'

section_list = []
tile_list = []
working_section = -1

for img in os.listdir(in_dir): # loop through in_dir
    section_num = int(img[15:18]) # find section number
    
    if section_num >= 551: # start from section 551
        path = in_dir + img
        
        if working_section == -1: # for first section
            path = in_dir + img
            tile_list.append(path)
            working_section = section_num
            
        elif section_num == working_section: # if it's the same section, make a list
            path = in_dir + img
            tile_list.append(path)
            
        else: # once you get to the new section, append tile list to section list, and move on
            section_list.append(tile_list)
            tile_list = []
            tile_list.append(path)
            working_section = section_num


# generate list of x and y coordinates
x_list = [0,3600,7200,10800,14400]*5*int(len(section_list))
y_list = [0,0,0,0,0,3600,3600,3600,3600,3600,7200,7200,7200,7200,7200,10800,
          10800,10800,10800,10800,14400,14400,14400,14400,14400]*int(len(section_list))

path_list = []
z_list = []

z = 0
for section in section_list:
    
    for tile in section:
        path_list.append(tile)
        z_list.append(z)
    z +=1

df = pd.DataFrame({'path': path_list, 'x': x_list, 'y': y_list, 'z': z_list})

save_name = in_dir + 'tile_positions.csv'
df.to_csv(save_name, header = None, index = None)