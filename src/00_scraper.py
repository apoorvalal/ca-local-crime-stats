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

# %% [raw]
# !pip install selenium lxml

# %%
import pandas as pd
import time, os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select

# %%
options = Options()

options.add_experimental_option("prefs", {
      "download.default_directory": r"/tmp",
      "download.prompt_for_download": False,
      "download.directory_upgrade": True,
      "safebrowsing.enabled": True
    })

options.add_argument('headless')
options.add_argument('--disable-infobars')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
# options.add_argument('--remote-debugging-port=9222')

driver = webdriver.Chrome('/home/alal/Desktop/Programs/chromedriver', options=options)

driver.get('https://openjustice.doj.ca.gov/exploration/crime-statistics/crimes-clearances')

# %% [markdown]
# # Scraper

# %% [markdown]
# ## First run - extract total number of cities etc

# %%
box = driver.find_element_by_xpath('//*[@id="ncic_chosen"]')
box.click()
box.find_element_by_xpath('//*[@id="ncic_chosen"]/div/ul')
dropdown_list = box.find_elements_by_xpath("//*[@class='active-result']")
city = dropdown_list[0]
cityname = city.text
print(cityname)

# %%
ncities = len(dropdown_list)
print(ncities)

# %% [markdown]
# ## Loop over cities

# %%time
for i in range(ncities+1):
    # refresh browser
    driver.refresh()
    time.sleep(1)
    # go to county dropdown
    box = driver.find_element_by_xpath('//*[@id="ncic_chosen"]')
    box.click()
    # list of cities
    box.find_element_by_xpath('//*[@id="ncic_chosen"]/div/ul')
    dropdown_list = box.find_elements_by_xpath("//*[@class='active-result']")
    # get current city
    city = dropdown_list[i]
    cityname = city.text
    print(cityname)
    city.click()
    # select crime radio button
    driver.find_element_by_xpath('//*[@id="crimes"]').click()
    time.sleep(.1)
    # get data
    driver.find_element_by_xpath('//*[@id="getRecord"]').click()
    time.sleep(1)
    # download
    driver.find_element_by_xpath('//*[@id="tblResult_wrapper"]/div[1]/button[1]').click()
    time.sleep(2)
    # move from temp location
    os.rename("/tmp/State of California Department of Justice - OpenJustice.csv",
          f"/home/alal/Desktop/LongSHOT/scrape/csvs/{cityname}.csv")
    if i % 20 == 0:
        print(f"{i} cities done; taking a break")
        time.sleep(10)

# %%
driver.close()
 #######  ##       ########
##     ## ##       ##     ##
##     ## ##       ##     ##
##     ## ##       ##     ##
##     ## ##       ##     ##
##     ## ##       ##     ##
 #######  ######## ########
# %% [markdown]
# # Older Data (2000 - 2009) dry run
box = driver.find_element_by_xpath('//*[@id="stats_year_range_chosen"]')
box.click()
dropdown_list = box.find_elements_by_xpath("//*[@class='active-result']")
oldwave = dropdown_list[9] # 2000 - 2009
oldwave.click()

# %% 2000 - 2009
for i in range(0, 870):
    # refresh browser
    driver.refresh()
    time.sleep(1)
    # year dropdown
    box = driver.find_element_by_xpath('//*[@id="stats_year_range_chosen"]')
    box.click()
    dropdown_list = box.find_elements_by_xpath("//*[@class='active-result']")
    oldwave = dropdown_list[9] # 2000 - 2009
    oldwave.click()
    # go to county dropdown
    box = driver.find_element_by_xpath('//*[@id="ncic_chosen"]')
    box.click()
    # list of cities
    box.find_element_by_xpath('//*[@id="ncic_chosen"]/div/ul')
    dropdown_list = box.find_elements_by_xpath("//*[@class='active-result']")
    # get current city
    city = dropdown_list[i]
    cityname = city.text
    print(cityname)
    city.click()
    # select crime radio button
    driver.find_element_by_xpath('//*[@id="crimes"]').click()
    time.sleep(.1)
    # get data
    driver.find_element_by_xpath('//*[@id="getRecord"]').click()
    time.sleep(1)
    # download
    driver.find_element_by_xpath('//*[@id="tblResult_wrapper"]/div[1]/button[1]').click()
    time.sleep(2)
    # move from temp location
    os.rename("/tmp/State of California Department of Justice - OpenJustice.csv",
          f"/home/alal/Desktop/LongSHOT/scrape/csvs/{cityname}_00_09.csv")
    if i % 20 == 0:
        print(f"{i} cities done; taking a break")
        time.sleep(10)

driver.close()

# %% 1990 - 1999
for i in range(0, 869):
    # refresh browser
    driver.refresh()
    time.sleep(1)
    # year dropdown
    box = driver.find_element_by_xpath('//*[@id="stats_year_range_chosen"]')
    box.click()
    dropdown_list = box.find_elements_by_xpath("//*[@class='active-result']")
    oldwave = dropdown_list[19] # 2000 - 2009
    oldwave.click()
    # go to county dropdown
    box = driver.find_element_by_xpath('//*[@id="ncic_chosen"]')
    box.click()
    # list of cities
    box.find_element_by_xpath('//*[@id="ncic_chosen"]/div/ul')
    dropdown_list = box.find_elements_by_xpath("//*[@class='active-result']")
    # get current city
    city = dropdown_list[i]
    cityname = city.text
    print(cityname)
    city.click()
    # select crime radio button
    driver.find_element_by_xpath('//*[@id="crimes"]').click()
    time.sleep(.1)
    # get data
    driver.find_element_by_xpath('//*[@id="getRecord"]').click()
    time.sleep(1)
    # download
    driver.find_element_by_xpath('//*[@id="tblResult_wrapper"]/div[1]/button[1]').click()
    time.sleep(2)
    # move from temp location
    os.rename("/tmp/State of California Department of Justice - OpenJustice.csv",
          f"/home/alal/Desktop/LongSHOT/scrape/csvs/{cityname}_90_99.csv")
    if i % 20 == 0:
        print(f"{i} cities done; taking a break")
        time.sleep(10)

driver.close()
