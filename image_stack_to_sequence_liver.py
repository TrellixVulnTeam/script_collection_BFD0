# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 13:34:57 2021
@author: Ben Mulcahy

Takes tiff stack and converts to serial images.
Made to process liver montage stacks from the SBF-SEM
"""

import os
from skimage import io, exposure, util

# change in_dir and out_dir to desired paths
in_dir = 'E:/temp_liver/' 
outdir = 'E:/temp_liver_series/'

# loop through stacks in directory
for stack in os.listdir(in_dir):
    if stack.endswith('.tif'): # select only .tif
        path = in_dir + stack
        im = io.imread(path) # opens image with skimage into 3d array
        tile_index = 0
        
        # loop through tiles in stack
        for tile in im:
            tile_clahe = exposure.equalize_adapthist(tile, clip_limit=0.03) # perform clahe
            tile_int = util.img_as_uint(tile_clahe) # have to convert from float64 array to int array
            tilename = stack[:-4] # crop '.tif' from the end
            
            # save with numberpadded tile number
            saveName = outdir + tilename + '_' + str(tile_index).zfill(2) + '.tif'
            io.imsave(saveName, tile_int)
            tile_index += 1
        print('Finished converting: \'' + stack + '\'')
        
        
