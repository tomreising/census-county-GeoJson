# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 20:05:31 2022

@author: tarei
"""
### for goepandas on windows download the GDAL and Fiona .whl files from
### https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal
### note that you have to download the .whl file associated with the your local python version
### ie. Fiona‑1.8.21‑cp310‑cp310‑win_amd64.whl would be used if running python 3.10 on win64 system
### after downloading move to a local folder then pip install GDAL first then Fiona
### after these steps you should be able to run pip install geopandas withou issue
import geopandas as gp
import os
#%%

# read in the county shapefile downloaded from us census data
# and save file as geoJson
path = os.getcwd()

df_county = gp.read_file(path+"\\cb_2018_us_county_20m\\cb_2018_us_county_20m.shp")
x = df_county.explore()
x.save(path+"\\cb_2018_us_county_20m\\countyMap.html")
df_county.to_file(path+"\\counties.json", driver='GeoJSON')
#%%
# read in geoJson
import json
with open(path+"\\counties.json", 'r') as fl:
    count_json = json.load(fl)
#%%
# prep vars for mapping, note GEOID in pandas df must map to GEOID in geoJson 
import pandas as pd
import numpy as np
col1 = df_county['GEOID'].to_list()
col2 = [np.random.random_integers(1,len(col1),1)[0] for i in range(len(col1))]

df_j_county = pd.DataFrame({'GEOID' : col1, 'colordf' : col2 })

#%%
# Plot 
import plotly
import plotly.express as px

fig = px.choropleth_mapbox(df_j_county, geojson=count_json,
                           featureidkey = 'properties.GEOID',
                           locations='GEOID', color='colordf',
                           color_continuous_scale="Viridis",
                           range_color=(0, 12),
                           mapbox_style="carto-positron",
                           zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                           opacity=0.5,
                           labels={'unemp':'unemployment rate'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

fig.add_scattermapbox(
    lat = [41.506346249673946],
    lon = [-93.57200875290822],
    mode = 'markers+text',
    #text = texts,
    marker_size=12,
    marker_color='rgb(235, 0, 100)'
)
plotly.offline.plot(fig)
