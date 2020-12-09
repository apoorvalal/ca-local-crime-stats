# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.3.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
# system
import os, sys, glob, re, itertools, collections, requests
import multiprocessing # parallelise list comprehensions
from pathlib import Path
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
font = {'family' : 'IBM Plex Sans',
               'weight' : 'normal',
               'size'   : 10}
plt.rc('font', **font)
plt.rcParams['figure.figsize'] = (10, 10)
matplotlib.style.use(['seaborn-talk', 'seaborn-ticks', 'seaborn-whitegrid'])
# %matplotlib inline
# %config InlineBackend.figure_format = 'retina'

# show all output
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = 'all'

# %%
import locale
from locale import atof
locale.setlocale(locale.LC_NUMERIC, '')

# %%
root = Path('/home/alal/Dropbox/1_Research/LongSHOT')
inp = root/'input'
tmp = root/'tmp'


# %% [markdown]
# # Function to slice and clean data

# %%
def make_header(df, stub):
    new_header = [stub + "__" + x.replace(" ", "_").replace("-","_") for x in df.iloc[0]]
    df = df[1:]
    df.columns = new_header
    return df


# %%
def data_cleaner(fn, splitu = False):
    name = fn.split('/')[-1]
    county_name, lea_name = name.split('-')[0].strip().replace("Co.", "") , name.split('-')[1].strip().split('.')[0]
    if splitu:
        county_name = name.split('-')[0].strip().replace("Co.", "") 
        lea_name = name.split('-')[1].strip().split('.')[0].split('_')[0]   
    df = pd.read_csv(fn)
    # slice and transpose rows from raw messy dataframe
    v_crimes   = make_header(df.loc[1:6].T, "vio_crimes_n")
    v_weapons  = make_header(df.loc[8:11].T, "vio_crimes_weap")
    v_location = make_header(df.loc[13:20].T, "vio_crimes_loc")
    p_crimes   = make_header(df.loc[26:27].T, "prop_crimes_n")
    p_type     = make_header(df.loc[46:54].T, "prop_crimes_type")
    # merge them by year, add county, LEA, and year 
    outdf = (pd.concat([v_crimes, v_weapons, v_location, p_crimes, p_type], axis = 1))
    outdf['county'] = county_name
    outdf['LEA'] = lea_name
    rest = [x for x in outdf.columns if x not in ['county', 'LEA']]
    outdf = outdf[['county', 'LEA'] + rest].reset_index().rename({'index':'year'}, axis = 1)
    return outdf


# %% [markdown]
# # 2010 - 2019

# %%
crime_root = root/"scrape/csvs/10_19"
# %cd $crime_root

# %%
files = glob.glob("*.csv")
files.sort()
files[:5]

# %% [markdown]
# ## Raw data

# %%
df = pd.read_csv("Los Angeles Co. - Los Angeles.csv")
df

# %% [markdown]
# ## dry run on LA data

# %%
odf = data_cleaner("Los Angeles Co. - Los Angeles.csv")
odf

# %% [markdown]
# numbers are still in string format at the moment - will clean at once with final dataset to avoid accounting for very small towns with no commas.

# %% [markdown]
# ## Apply to all places and stack

# %%
# %%time 
crime_cleaned = [data_cleaner(f) for f in files]

# %%
all = pd.concat(crime_cleaned, axis = 0).convert_dtypes()
all.info()

# %%
num_cols = all.columns[3:]
all[num_cols] =  (all[num_cols]
                  .astype('str') # convert 'objects' to string - pandas is too flexible 
                  .apply(lambda x: x.replace("--", "0")) # replace pesky -- empty rows
                  .applymap(atof) # convert to numeric by parsing commas 
                 )

# %% [markdown]
# ## sanity check

# %%
ladat = all.query("LEA == 'Los Angeles'")
ladat.head()
ladat.describe()

# %%
all = all.convert_dtypes() # compress to smallest possible data types

# %%
all.to_csv(root/'output/openjustice_place_panel_2010_2019.csv', index = False)

# %% [markdown]
# # 2000-2009

# %%
crime_root = root/"scrape/csvs/00_09"
# %cd $crime_root

# %%
files = glob.glob("*.csv")
files.sort()
files[:5]

# %%
# %%time 
crime_cleaned = [data_cleaner(f, splitu = True) for f in files]

# %%
all = pd.concat(crime_cleaned, axis = 0).convert_dtypes()
all.info()

# %%
num_cols = all.columns[3:]
all[num_cols] =  (all[num_cols]
                  .astype('str') # convert 'objects' to string - pandas is too flexible 
                  .apply(lambda x: x.replace("--", "0")) # replace pesky -- empty rows
                  .applymap(atof) # convert to numeric by parsing commas 
                 )

# %%
all.head()

# %%
all = all.convert_dtypes() # compress to smallest possible data types

# %%
all.to_csv(root/'output/openjustice_place_panel_2000_2009.csv', index = False)

# %% [markdown]
# # 1990 -1999

# %%
crime_root = root/"scrape/csvs/90_99"
# %cd $crime_root

# %%
files = glob.glob("*.csv")
files.sort()
files[:5]

# %%
# %%time 
crime_cleaned = [data_cleaner(f, splitu = True) for f in files]

# %%
all = pd.concat(crime_cleaned, axis = 0).convert_dtypes()
all.info()

# %%
num_cols = all.columns[3:]
all[num_cols] =  (all[num_cols]
                  .astype('str') # convert 'objects' to string - pandas is too flexible 
                  .apply(lambda x: x.replace("--", "0")) # replace pesky -- empty rows
                  .applymap(atof) # convert to numeric by parsing commas 
                 )

# %%
all.head()

# %%
all = all.convert_dtypes() # compress to smallest possible data types

# %%
all.to_csv(root/'output/openjustice_place_panel_1990_1999.csv', index = False)

# %% [markdown]
# ## Stack

# %%
df1 = pd.read_csv(root/'output/openjustice_place_panel_1990_1999.csv')
df2 = pd.read_csv(root/'output/openjustice_place_panel_2000_2009.csv')
df3 = pd.read_csv(root/'output/openjustice_place_panel_2010_2019.csv')

# %%
df = pd.concat([df1, df2, df3])
df.sort_values(['county', 'LEA', 'year'], inplace = True)

# %%
df.info()

# %%
df.to_csv(root/'output/openjustice_place_panel_1990_2019.csv', index = False)
