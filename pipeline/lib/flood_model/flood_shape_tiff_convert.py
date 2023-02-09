# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 16:22:30 2022

@author: ATeklesadik
"""
import pandas as pd
from shapely.geometry import Point
import fiona
import matplotlib.pyplot as plt 
import geopandas as gpd 
import re
import json
import numpy as np
import os
import rioxarray
import rasterio as rio
from geocube.api.core import make_geocube
import xarray as xr
import glob

## convert and save flood extents which are in shapefiles to tiff 
 

 
zip_files = glob.glob('C:/Users/ATeklesadik/OneDrive - Rode Kruis/Documents/documents/philipiness/flood_model/25yr/*.zip')

tiff_fils_dir='C:/Users/ATeklesadik/OneDrive - Rode Kruis/Documents/documents/philipiness/flood_model/25yr/tiffs/'
population_data =rioxarray.open_rasterio("C:/Users/ATeklesadik/OneDrive - Rode Kruis/Documents/documents/IBF_FLOOD_PIPELINE/pipeline/data/raster/input/population/hrsl_phl_band1_.tif")

forecast_df=[]
for shpfile in zip_files:
    flood_disk = gpd.GeoDataFrame.from_file(shpfile)
    population_prov=population_data.rio.write_crs("epsg:4326", inplace=True).rio.clip(flood_disk.geometry.values, flood_disk.crs, from_disk=True).sel(band=1).drop("band")
    out_grid = make_geocube(
        vector_data=flood_disk,
        measurements=["Var"],
        like=population_prov, # ensure the data are on the same grid
    )
    filename=tiff_fils_dir+shpfile.split('\\')[-1].split('.')[0]
    out_grid["Var"].rio.to_raster(f"{filename}.tif")