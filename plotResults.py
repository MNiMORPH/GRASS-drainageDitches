# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 14:05:24 2024

@author: Uma
"""

import rioxarray
import matplotlib.pyplot as plt
import geopandas

# Path to clipped raster data
hucCode = '07080102'
hucDir = 'outputs/HUC_' + hucCode + '/'
hucFile = hucDir + 'HUC_' + hucCode + '.tif' 

# Path to shapefile
shpFile='basins/dnr_watersheds_dnr_level_04_huc_08_majors.shp'

# Read and reproject the subwatershed boundaries
geoDf = geopandas.read_file(shpFile)
df_4326=geoDf.to_crs("EPSG:4326")
subWS = df_4326[df_4326['HUC_8'] == hucCode]

# Open and reproject the subwatershed data
# Editing the long_name and units makes sure the axes and colorbar are labeled correctly
ras=rioxarray.open_rasterio(hucFile, masked=True).squeeze().rio.reproject("EPSG:4326")
ras.attrs['long_name'] = 'Elevation [m]'    # get units right
ras.x.attrs['long_name'] = 'Longitude'
ras.x.attrs['units'] = 'Degrees'
ras.y.attrs['long_name'] = 'Latitude'
ras.y.attrs['units'] = 'Degrees'

# Plot with HUC code as well as long name
fig, ax = plt.subplots(figsize=(10, 6))
ras.plot(ax=ax)
wsName = subWS['major_name'].iloc[0]
ax.set_title('HUC ' + hucCode + ': ' + wsName)

# Plot the watershed boundary over the rectangular raster data
subWS.boundary.plot(ax=ax, color='k')

ras.close()

