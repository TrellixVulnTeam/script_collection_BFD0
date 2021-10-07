# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 16:15:31 2021

take cell name and segment ID from VAST 3D surface export (via VASTtools) and 
make into a key for the boss.db neuroglancer datasets

@author: Ben Mulcahy
"""

import pandas as pd
import os

path = 'D:/vast_export_ID/temp/metadata/'

for f in os.listdir(path):
    if 'segmentation' in f:
        newpath = path + f

        df = pd.read_csv(newpath, delimiter = " ", skiprows = 6, header = None)
        df = df.dropna(how = 'all', axis = 'columns')
        df.columns = ['Nr','flags', 'red1', 'green1', 'blue1', 'pattern1', 'red2', 'green2', 'blue2', 'pattern2', 'anchorx', 'anchory', 'anchorz', 'parentnr', 'childnr', 'prevnr', 'nextnr', 'collapsednr', 'bboxx1', 'bboxy1', 'bboxz1', 'bboxx2', 'bboxy2', 'bboxz2', 'name']

        droplist = []
        for d in range(len(df)):
            f1 = df['name'][d]
            if f1.endswith('Cells'):
                droplist.append(d)
        
        df = df.drop(droplist)
        df = df.reset_index(drop=True)
        
        newdf = df[['name', 'Nr']].copy()
        newdf.columns=['Name', 'Segment_ID']
        newdf = newdf.sort_values('Name')
        
        # export to csv
        fsplit = f.split('_')
        dataset = fsplit[0]
        
        fname = path + dataset + '_segmentation_key.csv'
        newdf.to_csv(fname, index=False)