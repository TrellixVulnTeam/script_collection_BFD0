# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 14:18:17 2021

A script to generate tiles for CATMAID from flat images.
Will take all tiff files in the path folder and generate CATMAID-style tiles 
in the format 'row_column_zoom.jpg' inside folders corresponsing to section number. 

Make sure the tiff files are number padded appropriately, and are read in the correct order.

Change the path, tile size and number of zoom levels as needed.

@author: Ben Mulcahy
"""

import os
from skimage import io, util, transform

# change these as needed
path = "D:/temp/"
tile_size = 512
zoomlevels = 5

# make list of tif files in directory
file_list = []
for f in os.listdir(path):
    if f.endswith('.tif'):
        file_list.append(path + f)

file_list.sort() #sort alphabetically

tilepath = path + 'catmaid_tiles/' # new folder in which the tiles will be saved
os.makedirs(tilepath) 

z = 0 # to be used when generating folders for each section
for f in file_list:
    print(f)
    out_path = tilepath + str(z) + '/' # generate the folder for current section
    os.makedirs(out_path)
    
    img = io.imread(f)    
    
    # make catmaid tiles for each zoom level and save in format 'row_column_zoom.jpg'
    for zoom in range(zoomlevels):
        if zoom == 0: # if it's the first round, use full resolution image
            print('starting zoom 0')
        else:
            print('starting zoom', zoom)
            img = util.img_as_ubyte(transform.rescale(img, 0.5)) # need to specify ubyte otherwise it gets generated as float64, and a warning message about lossy conversion to utf-8 appears for every tile
        # extract dimensions and calculate number of rows and columns of tiles that will be generated
        y, x = img.shape
        n_row = int(y / tile_size)
        n_col = int(x / tile_size)
                
        # make the tiles and save in appropriate folder
        for r in range(n_row):
            row = r * tile_size
            for c in range(n_col):
                col = c * tile_size
                cropped = img[row:row+tile_size,col:col+tile_size]
                out_name = out_path + str(r) + '_' + str(c) + '_' + str(zoom) + '.jpg'
                io.imsave(out_name, cropped, check_contrast=False)
    z += 1

