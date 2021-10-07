# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 08:29:52 2021

Script to stitch dataset from catmaid tiles. Can choose the resolution.
Made for painting nuclei of motor neurons and precursors. 

Structure is folder for each section, then tiles named e.g. 1_1_5.jpg: row, column, zoom
the code will need to be modified for other formats

@author: Ben Mulcahy
"""
#%% modify the necessary parts of this section (path etc) and choose which block
# you want to use, to stitch all sections in the delected directory, or select sections

import os
from tkinter import *
from PIL import Image # this has to be imported after tkinter (maybe 'import *' wasn't so bright)
import sys

# change below as necessary
path = 'D:/Neeraja/TEM_adult/'
out_path = 'D:/Neeraja/stitched/' 
desired_zoomlevel = str(3) # change as necessary
numberpadding = 4 # numberpadding for output name
image_type = '.jpg' # '.jpg', '.png', or '.tif'

def set_m(m): # used to select mode (stitch all sections, even only, or a range)
    global mode
    mode = m
    root.destroy()
    
def retrieve(): # if the range mode is selected, retrieves the range values from the tkinter gui
    global start
    global end
    try:
        start = int(Entry1.get())
        end = int(Entry2.get())
    except:
        print('Error: start and end need to be integers')
    root.destroy()

# bring up a gui to select stitching mode
root = Tk()
frame = Frame(root)
frame.pack()
label = Label(frame, text = "Choose how you would like to stitch your tiles")
label.pack()
button1 = Button(frame, text = "All sections", command = (lambda: set_m('a')))
button1.pack(padx = 3, pady = 3)
button2 = Button(frame, text = "Even sections only", command = (lambda: set_m('e')))
button2.pack(padx = 3, pady = 3)
button3 = Button(frame, text = "Define a range of sections", command = (lambda: set_m('r')))
button3.pack(padx = 3, pady = 3)
root.title("Select mode")
root.mainloop() # triggers GUI
 
section_list = []
if mode == 'a': # stitch all sections
    for d in os.listdir(path):
        if os.path.isdir(os.path.join(path, d)):
            section_list.append(path + d) # make a list of sections to stitch
            
elif mode == 'e': # stitch even sections only
    for d in os.listdir(path):
         if int(d) % 2 == 0:
             if os.path.isdir(os.path.join(path, d)):
                 section_list.append(path + d) # make a list of sections to stitch
                 
elif mode == 'r': # stitch a defined range of sections 
    root = Tk()
    frame = Frame(root)
    frame.pack()
    Entry1 = Entry(frame, width = 10)
    Entry1.grid(row=0, column=1,padx = 10, pady = 10)
    Label1 = Label(frame)
    Label1.configure(text="First Section:")
    Label1.grid(row=0, column=0,padx = 5, pady = 10)
    Entry2 = Entry(frame, width = 10)
    Entry2.grid(row=1, column=1,padx = 10, pady = 10)
    Label2 = Label(frame)
    Label2.configure(text="Last Section:")
    Label2.grid(row=1, column=0,padx = 5, pady = 10)
    button1 = Button(frame, text = "Submit", command = (lambda: retrieve()))
    button1.grid(row = 2, column = 1, padx = 10, pady = 10)
    root.title("Specify start and end slices")
    root.mainloop()

    for d in os.listdir(path):
        if os.path.isdir(os.path.join(path, d)):
            if int(d) < start:
                continue
            if int(d) < end:
                section_list.append(path + d) # make a list of sections to stitch
    
#%% Run to stitch and export jpgs of the desired zoom level to the out path

# find dimensions
tile_list = []
for s in section_list:
    # make list of tiles    
    for tile in os.listdir(s):
        if tile.endswith(desired_zoomlevel + image_type):
            tile_list.append(tile)

# find tilesize
eg_tilepath = s + "/" + tile
eg_tile = Image.open(eg_tilepath)
width, height = eg_tile.size
if width == height:
    tilesize = width
else:
    sys.exit("Error: tile width and height are not equal dimensions")

# extract dimensions from tile names
ncol = 0
nrow = 0
for tile in tile_list:
    [y,x,zm] = tile.split("_")
    if int(x) > ncol:
        ncol = int(x)
    if int(y) > nrow:
        nrow = int(y)
total_width = tilesize * (ncol + 1)
total_height = tilesize * (nrow + 1)

# loop through sections
for s in section_list:
    # add tiles of desired zoom level to list
    tile_list = []
    for tile in os.listdir(s):
        if tile.endswith(desired_zoomlevel + image_type):
            tile_list.append(tile)
        ntiles = len(tile_list)
    
    # create empty image of correct dimensions
    new_im = Image.new('L',(total_width, total_height)) # 'L' is 8-bit black and white
    
    for tile in tile_list:
        tilepath = s + "/" + tile
        [tile_y, tile_x, mag] = tile.split("_") # get row and column of tiles
        x = int(tile_x) * tilesize # convert to pixel position
        y = int(tile_y) * tilesize
        image = Image.open(tilepath)
        new_im.paste(image, box = (x,y)) # box is upper left pixel coordinate
    #new_im.show() # opens the image in a new window
    
    # numberpad
    section = os.path.basename(s)
    if len(section) != numberpadding:
        section = section.zfill(numberpadding)
    
    # save to the out path
    section_name = out_path + 'section_' + section + image_type
    new_im.save(section_name)