# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
from PIL import Image
import PIL.ImageOps    

path = 'C:/Users/mulcahy/Desktop/dauer_mEMbrain/GT3_2021_07_19/temp/'

for f in os.listdir(path):
    fpath = path + f
    image = Image.open(fpath)
    inverted_image = PIL.ImageOps.invert(image)
    inverted_image.save(fpath)
