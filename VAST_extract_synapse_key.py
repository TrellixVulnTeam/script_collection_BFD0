# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 16:27:52 2021

take names and segment ID from VAST 3D surface export (via VASTtools) and
make into a key for the boss.db neuroglancer datasets for the synapse data

@author: Ben Mulcahy
"""

import pandas as pd
import os


path = 'D:/vast_export_ID/temp/metadata/'

for f in os.listdir(path):
    if 'synapse' in f:
        newpath = path + f

        df = pd.read_csv(newpath, delimiter = " ", skiprows = 6, header = None)
        df = df.dropna(how = 'all', axis = 'columns')
        df.columns = ['Nr','flags', 'red1', 'green1', 'blue1', 'pattern1', 'red2', 'green2', 'blue2', 'pattern2', 'anchorx', 'anchory', 'anchorz', 'parentnr', 'childnr', 'prevnr', 'nextnr', 'collapsednr', 'bboxx1', 'bboxy1', 'bboxz1', 'bboxx2', 'bboxy2', 'bboxz2', 'name']

        droplist = []
        for d in range(len(df)):
            f1 = df['name'][d]
            if f1.endswith('synapses'):
                droplist.append(d)

        df = df.drop(droplist)
        df = df.reset_index(drop=True)
        df = df.sort_values('name')
        df = df.reset_index(drop=True)



        label = df['name']

        synapses = []
        for x in label:
            split1 = x.split(' ')
            synapses.append([split1[0],split1[1]])


        synapse_df = pd.DataFrame(synapses)
        synapse_df.columns = ['Presynaptic', 'Postsynaptic']

        newdf = df[['Nr', 'anchorx', 'anchory', 'anchorz']].copy()
        newdf.columns=['Segment_ID', 'X-pos', 'Y-pos', 'Z-pos']
        newdf['X-pos'] = 2 * newdf['X-pos']
        newdf['Y-pos'] = 2 * newdf['Y-pos']

        final_df = pd.concat([synapse_df, newdf], axis=1)

        # export to csv
        fsplit = f.split('_')
        dataset = fsplit[0]

        fname = path + dataset + '_synapse_key.csv'
        final_df.to_csv(fname, index=False)
