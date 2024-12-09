# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 14:19:07 2024

@author: Uma
"""

import grass.script as gs
import pandas as pd
import math
import os

bufferFile = 'bufferShp.txt'    # name of file containing buffer around each subwatershed, whether the file exists yet or not
mapName = 'dnr_watersheds_dnr_level_04_huc_08_majors'   # vector layer in Grass GIS
hucLevel = 'HUC_8'   # column name in the shapefile metadata
rasterSource = 'D:/MinnesotaLiDAR.tif'  # path to DEM
outParentDir = 'outputs/'   # parent directory for subwatershed folders
#rasterSource = 'outputs/HUC_07080102.tif'
dataName = 'demSource'  # what the DEM (or link to it) is called in Grass

#%% Function definition

def createBoundingBox():
    """ Finds the extent of each subwatershed, 
    and calculates a rectangular bounding box padded by 100m 
    Outputs a DataFrame with the bounds and saves to file bufferFile"""
    
    # Grass GIS adds attribute columns with the extent of each subwatershed
    gs.run_command('v.to.db', map=mapName, option='bbox', \
                   columns=['n', 's', 'e', 'w'], overwrite=True)
        
    # Output the attribute table with the new columns as tmp.txt, and read it in
    gs.run_command('v.db.select', map=mapName, format='csv', file='tmp.txt')
    rawBox = pd.read_csv('tmp.txt', dtype={'HUC4': 'str', 'HUC_8': 'str'})
    bufferBox = rawBox.copy()

    # Round N and E extents up to nearest integer, and round S and W down
    # Pad the subwatershed extent with 100m on each side
    for upCol in ['n','e']:
        col2 = pd.Series([(math.ceil(item)+100) for item in rawBox[upCol]])
        bufferBox[upCol]=col2
        
    for downCol in ['s', 'w']:
        col2 = pd.Series([(math.floor(item)-100) for item in rawBox[downCol]])
        bufferBox[downCol]=col2
        
    bufferBox.to_csv(bufferFile, index=False)
    
    return bufferBox

def clipSubWS(n, s, e, w, filesName):
    """ Creates raster file of rectangular region around subwatershed
    
    n, s, e, w: region boundaries, usually inputted from the bounding box
    filesName: the HUC code for this subwatershed. This will be the raster file name """
    
    # Create separate directory for each subwatershed raster file
    outDir = outParentDir + filesName + '/'
    if not os.path.exists(outDir):
        os.mkdir(outDir)
        
    # Set computational region to padded bounding box, and save region as vector
    gs.run_command('g.region', flags='p', n=n, s=s, e=e, w=w)
    
    # Write DEM data to file - only writes current region
    gs.run_command('r.out.gdal', input=dataName, output=outDir + filesName+'.tif', \
                   type='Float32', format='GTiff', createopt="COMPRESS=LZW,BIGTIFF=YES", flags='f')
    
#%% Loop through subwatersheds to extract data

# Check if bounding-box text file exists, and either read it or create it
if os.path.exists(bufferFile):
    bufferBox = pd.read_csv(bufferFile, dtype={'HUC4': 'str', 'HUC_8': 'str'})
else:
    bufferBox = createBoundingBox()
    
# Link to external raster data without reading it in
gs.run_command('r.external', input=rasterSource, output=dataName, flags='r')
    
for subWS in bufferBox:
    
    hucCode = 'HUC_' + str(subWS[hucLevel])
    n, s, e, w = subWS['n'], subWS['s'], subWS['e'], subWS['w']
    clipSubWS(n, s, e, w, hucCode)

