# -*- coding: utf-8 -*-
"""
Spyder Editor
@author: Ben Mulcahy

Inverts all images inside a specified directory
"""
import os
from PIL import Image
import PIL.ImageOps    

path = 'C:/Users/mulcahy/Desktop/dauer_mEMbrain/GT3_2021_07_19/temp/' # change as necessary

# loop through all images in path, invert them and save them back to original location (overwrite)
for f in os.listdir(path):
    fpath = path + f
    image = Image.open(fpath)
    inverted_image = PIL.ImageOps.invert(image)
    inverted_image.save(fpath)
