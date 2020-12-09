# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.3.3
#   kernelspec:
#     display_name: 'Env: Geo'
#     language: python
#     name: gds
# ---

# %%
# system
import os, sys, glob, re, itertools, collections, requests
import multiprocessing # parallelise list comprehensions
from pathlib import Path

# filler to import personal library
# sys.path.append('/home/alal/Desktop/code/py_libraries/')

# pyscience imports
import numpy as np
import pandas as pd
import janitor
import pandas_flavor as pf
import statsmodels.api as sm
import statsmodels.formula.api as smf

# viz
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from plotnine import *
sns.set(style="ticks", context="talk")
font = {'family' : 'IBM Plex Sans',
               'weight' : 'normal',
               'size'   : 10}
plt.rc('font', **font)
plt.rcParams['figure.figsize'] = (10, 10)
matplotlib.style.use(['seaborn-talk', 'seaborn-ticks', 'seaborn-whitegrid'])
# %matplotlib inline
# %config InlineBackend.figure_format = 'retina'

# geodata packages
import geopandas as gpd
import geoplot as gplt
import contextily as cx
# raster packages
# import rasterio as rio
# from rasterstats import zonal_stats

# show all output
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = 'all'

# %% [markdown]
# # Ingest

# %% [markdown]
# ## Spatial

# %%
root = Path('/home/alal/Dropbox/1_Research/LongSHOT')
inp = root/'input'
tmp = root/'tmp'

# %%
lea = (gpd.read_file(inp/"Local_Law_Enforcement_Locations/Local_Law_Enforcement.shp")
       .clean_names()
       .infer_objects())
lea.info()

# %% [markdown]
# ## Clean

# %%
lea_ca = lea.query("state == 'CA'")

# %%
lea.shape
lea_ca.shape

# %%
place = (gpd.read_file(inp/'tl_2019_06_place/tl_2019_06_place.shp')
        .clean_names()
        .infer_objects())
place.info()

# %%
place.crs
lea.crs

# %% [markdown]
# ## Reproject

# %%
lea_ca = lea_ca.to_crs("EPSG:4326")
place = place.to_crs("EPSG:4326")

# %% [markdown]
# ## Preliminary map

# %%
f, ax = plt.subplots(figsize = (10, 12), dpi = 150)
place.plot(facecolor = 'None', edgecolor = 'r', ax = ax)
lea_ca.plot(ax = ax, facecolor = 'green', markersize = 1)
cx.add_basemap(ax, crs = place.crs.to_string(),
               source = cx.providers.Stamen.TonerLite)
ax.set_title("CA LEAs and Census Places")
ax.set_axis_off()

# %% [markdown]
# ## spatial merge 

# %%
merged = gpd.sjoin()
