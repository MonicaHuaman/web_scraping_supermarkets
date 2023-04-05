# Import Modules
from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime
import random
import os
import web_scrp_func

# User agents
headers = {'User-Agent': web_scrp_func.GET_UA()}

# 1.- WEBSCRAPING OF AHORRAMAS
supermarket = "ahorramas"

# Get all the urls of Ahorramas
dict_info = web_scrp_func.DICT_INFO_SUPERMARKET(supermarket)

# Create empty data frame
df_total = pd.DataFrame(columns=['Name','Price','URL','Keyword'])

# Make a loop for all the URLS in Aho
# rramas
for keyword in dict_info.keys():
    # Get the URLS
    url_text = dict_info[keyword]
    # Get the information of the webpage
    soup = web_scrp_func.GET_URL_INFO(url_text,headers)
    # Get the information of names, prices and Urls
    df_info = web_scrp_func.CLEAN_DATA_AHORRAMAS(soup,keyword)
    df_total = df_total.append(df_info)
    print("done")

# Export to excel
df_total.to_excel(".\Downloads\Prices_" + supermarket + "_" + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + ".xlsx",index=False)

# 2.- WEBSCRAPING OF DIA
supermarket = "dia"

# Get all the urls of Ahorramas
dict_info = web_scrp_func.DICT_INFO_SUPERMARKET(supermarket)

# Create empty data frame
df_final = pd.DataFrame()

# Make a loop for all the URLS in Dia
for keyword in dict_info.keys():
    # Get the URLS
    url_text = dict_info[keyword]
    # Get the information of the webpage
    soup = web_scrp_func.GET_URL_INFO(url_text,headers)
    # Get the information of names, prices and Urls
    df_info = web_scrp_func.CLEAN_DATA_DIA(url_text,soup,keyword,headers)
    df_final = df_final.append(df_info)
    print("done")

# Export to excel
df_final.to_excel(".\Downloads\Prices_" + supermarket + "_" + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + ".xlsx",index=False)
