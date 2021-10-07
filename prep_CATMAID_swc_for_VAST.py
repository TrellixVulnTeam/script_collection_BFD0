# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 16:01:07 2021
@author: Ben Mulcahy

Takes swc files that have been exported from CATMAID and prepares them for import into VAST
"""

import os
import pandas as pd

# folder containing swc files
swc_dir = 'C:/Users/zhenlab/Desktop/temp/Stigloher_dauer_3_catmaid-swc-export/'

# loop through files in dir
for f in os.listdir(swc_dir):
    
    if f.endswith('.swc'): # only process files that end in '.swc'
    
        swc_path = swc_dir + f
    
        # read the swc file
        df = pd.read_csv(swc_path, sep=' ', header=None)
        
        # convert z scale from 5nm to 8nm (for Stigloher_dauer_3, the CATMAID z resolution is 
        # incorrectly set at 5nm, but should be 8nm)
        df[4] = (df[4] / 5) * 8
        
        # convert to um (because this is what VAST takes)
        df[2] = df[2]/1000
        df[3] = df[3]/1000
        df[4] = df[4]/1000
        
        # save the csv
        out_name = swc_dir + f
        df.to_csv(out_name, sep=' ', header=None, index = False)


