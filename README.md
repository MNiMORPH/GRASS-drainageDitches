# GRASS-drainageDitches
Using Grass GIS to split up a large dataset into sub-watersheds.

### Research problem, and data sources
The goal is to find sites for drainage ditch removal (and therefore wetland restoration) in Minnesota. Using an elevation map, we want to run a model that shows where water pools and flows in the landscape, giving us the current wetland extent. Later, we will simulate removing the drainage ditches, and see how this changes wetland extent and hydrological connectivity.

#### **_Data sources_**
- **Minnesota digital elevation model (DEM)**. I am using 1-m resolution elevation data. In GIS, this is an example of **raster** data, because the shape of Minnesota is filled in with evenly-spaced elevation data. (Think of a coloring page that has been colored in: raster data are like the continuous colors inside the lines.) Raster data often comes with the .tif file extension.
- **Subwatershed boundaries**. These boundaries are called Hydrologic Unit Codes (HUC), set by the US Geological Survey. There are different scales of sub-watersheds, and HUC represents these with the number of digits in the unit code. For example, 4-digit codes are called HUC4, but if you want to get more specific and break these sub-watersheds down further, you would use 8-digit codes called HUC8. In GIS, watershed boundaries are an example of **vector** data, because they are only outlines. (It's like a coloring page that has been left blank, so we only see the lines.) Vector data can have the .shp file extension.

Using the watershed boundaries, we will break down the digital elevation model into manageable sizes, and run the model on each of these smaller units.

### What is Grass GIS, and why is it a good option for large datasets?

Because of its fine resolution, the Minnesota DEM I'm using is almost 3 TB! Even when I broke it down into HUC8 watersheds, which are moderately sized, they were still too much for my computer's memory when I tried to read them in using Python. Python reads in all data from the subwatershed at once and tries to keep it in memory. On the other hand, Grass GIS can read in one byte of data at a time, write it to a file, and then free it from memory before repeating with the next byte of data.

You can install it from the [GRASS download link](https://grass.osgeo.org/download/).

Installation and using with Python
- file structure

Notes about the code

Results
  
