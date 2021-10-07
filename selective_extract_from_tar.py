# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 14:06:01 2021

used to extract CATMAID tiles at only zoom level 4 from tar file
had to do it this way becaus tar file was 488GB, not enough storage to extract everything

will extract to working directory

@author: Ben Mulcahy
"""

import tarfile

path = 'D:/for_nuclei/SEM_L1_3/SEM_L1_3_catmaid_export.tar'

t = tarfile.open(path, 'r')

#print(t.list(verbose=False)) #prints list of files

with tarfile.open(path) as tar:
    subdir_and_files = [
        tarinfo for tarinfo in tar.getmembers()
        if tarinfo.name.endswith('4.jpg') # change this as necessary
    ]
    tar.extractall(members=subdir_and_files)
