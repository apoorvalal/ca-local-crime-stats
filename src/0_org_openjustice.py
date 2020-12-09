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
from pathlib import Path
import os, glob

# %%
root = Path('/home/alal/Dropbox/1_Research/LongSHOT')
inp = root/'input'
tmp = root/'tmp'

# %% [markdown]
# ### Organise bulk downloads into subfolders

# %%
scraped = root/'scrape/csvs/'
scraped
# %cd $scraped

# %%
csvs = glob.glob("*.csv")
csvs.sort()
csvs[:5]

# %%
csvs_09 = glob.glob("*_09.csv") 
csvs_99 = glob.glob("*_99.csv")
csvs_old = csvs_09 + csvs_99
csvs_old.sort()
csvs_old[:5]

# %%
new_files = [c for c in csvs if c not in csvs_old]
new_files.sort()
new_files[:5]

# %%
Path(scraped/'10_19').mkdir(parents = True, exist_ok = True)
Path(scraped/'00_09').mkdir(parents = True, exist_ok = True)
Path(scraped/'90_99').mkdir(parents = True, exist_ok = True)

# %%
[os.rename(c, '10_19/' + c) for c in new_files]

# %%
[os.rename(c, '00_09/' + c) for c in csvs_09]

# %%
[os.rename(c, '90_99/' + c) for c in csvs_99]

# %%
