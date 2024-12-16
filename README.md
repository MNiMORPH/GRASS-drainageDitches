# GRASS-drainageDitches
Using Grass GIS to split up a large dataset into sub-watersheds. Featuring some things I learned about Grass GIS and GIS in general.

### Research problem, and data sources
The goal is to find sites for drainage ditch removal (and therefore wetland restoration) in Minnesota. Using an elevation map, we want to run a model ([Fill-Spill-Merge](https://github.com/r-barnes/Barnes2020-FillSpillMerge.git)) that shows where water pools and flows in the landscape, giving us the current wetland extent. Later, we will simulate removing the drainage ditches, and see how this changes wetland extent and hydrological connectivity.

#### **_Data sources_**
- **Minnesota digital elevation model (DEM)**. I am using 1-m resolution elevation data. In GIS, this is an example of **raster** data, because the shape of Minnesota is filled in with evenly-spaced elevation data. (Think of a coloring page that has been colored in: raster data are like the continuous colors inside the lines.) Raster data often comes with the .tif file extension.
- **Subwatershed boundaries**. These boundaries are called Hydrologic Unit Codes (HUC), set by the US Geological Survey, and can be downloaded [here](https://mnatlas.org/resources/watersheds-dnr-level-4/). There are different scales of sub-watersheds, and HUC represents these with the number of digits in the unit code. For example, 4-digit codes are called HUC4, but if you want to get more specific and break these sub-watersheds down further, you would use 8-digit codes called HUC8. In GIS, watershed boundaries are an example of **vector** data, because they are only outlines. (It's like a coloring page that has been left blank, so we only see the lines.) Vector data can have the .shp file extension.

Using the watershed boundaries, we will break down the digital elevation model into manageable sizes, and run the model on each of these smaller units.

### What is Grass GIS, and why is it a good option for large datasets?

Because of its fine resolution, the Minnesota DEM I'm using is almost 3 TB! Even when I broke it down into HUC8 watersheds, which are moderately sized, they were still too much for my computer's memory when I tried to read them in using Python. Python reads in all data from the subwatershed at once and tries to keep it in memory. On the other hand, Grass GIS can read in one byte of data at a time, write it to a file, and then free it from memory before repeating with the next byte of data. (If you are working with smaller data and want to do this all in Python, I recommend [Jesse's drainage ditches code](https://github.com/jesse-schewe/DrainageDitches.git).)

GRASS is also free and open source. You can install it from the [GRASS download link](https://grass.osgeo.org/download/).

Once you open the user interface, you will see a few different levels in the file structure. There are databases, which have projects/locations inside of them, with mapsets inside of those. I like the diagram and explanations on the [GRASS file structure page](https://grass.osgeo.org/grass-stable/manuals/grass_database.html). In the Data pane, use the cylinder icon to create a new database, and the globe icon to its right to create a project inside of the database. The project needs to be based on a data source, so use the shapefile (.shp) with the watershed boundaries. After that, GRASS will automatically create a mapset called PERMANENT for you. You can now start running commands and scripts.

### Python scripting

GRASS comes with its own commands, but it can also be used with Python scripts. This is especially helpful if you (like me) aren't too familiar with GRASS but know how to do something easily in Python, so you can combine their functionalities. 

The library you need to import in your Python script is called [grass.script](https://grass.osgeo.org/grass-stable/manuals/libpython/script_intro.html). There is no need to install the package using pip or conda; it comes with the GRASS installation. (Note: If you try to run the script in a Python IDE, it might not recognize the library, but if you run it through the GRASS user interface, it will run without error. I will explain how to do that next.) In the Tools panel of the GRASS interface, use the Python tab to change directories into wherever your script is located. Then in Console, type `python3 grassScript.py`, where grassScript is the file name of your script, which will run your script. If you don't want to type these commands, you could also go to **File > Launch script**. 

The syntax when running GRASS commands in Python is different from just running them in the GRASS interface. Let's say you want to run the command [g.region](https://grass.osgeo.org/grass-stable/manuals/g.region.html), which sets the computational region. In the GRASS Console, you would type in whatever flags and parameters you need, like `g.region -pm raster=elevation --verbose`. In a Python script, this would be:

```
import grass.script as gs  # only needed once 
gs.run_command("g.region", flags='pm', raster='elevation', verbose=True)
```

If you look at the documentation of any GRASS command, the flags with a single dash (like -p and -m in this example) go into `flags='pm'`, while the flags with two dashes (like --verbose) are turned on or off with the Boolean `verbose=True`. 

Finally, if your script uses something like NumPy or Pandas to process data, you may need to install them using Grass's Python tab, even if you have installed them on your computer already (there may be a way to avoid re-installation and just change directories, but I haven't figured it out yet.) In the Console tab, type `python3 -m pip install pandas` (or whichever package you want to install).

### Notes about the code

The Python script is called [grassScript.py](https://github.com/MNiMORPH/GRASS-drainageDitches/blob/main/grassScript.py).

The program starts by calculating the northern, southern, eastern, and western extents of each sub-watershed. These extents are often decimals, which can cause errors later on, in which the model incorrectly interpolates between them. To avoid this, we want to round them to a whole number now (round up for north and east, and round down for south and west.) Then, we will pad these extents by 100m to prevent any edge effects from the model, eventually creating a padded rectangular box around each sub-watershed.

It then creates a link to the DEM data, keeping it external so it doesn't have to read it all in. 

It loops through each rectangular bounding box, and outputs a file with the DEM cropped down to that region.

### Results

I used Python ([plotResults.py](https://github.com/MNiMORPH/GRASS-drainageDitches/blob/main/plotResults.py)) to view an example result and overlay the sub-watershed boundary over the rectangular region, but you could use GIS for this too. Note that in Python, you need the [geopandas](https://geopandas.org/en/stable/getting_started/install.html) and [rioxarray](https://corteva.github.io/rioxarray/html/installation.html) modules. 

![Elevation map with overlaid watershed boundary.](HUC8_07080102_padded.png?raw=true "HUC8_07080102")
  
