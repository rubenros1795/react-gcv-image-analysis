from bs4 import BeautifulSoup
import datetime
import pandas as pd
import requests
from collections import Counter
import string
import re as regexz
import random
import os.path
from tqdm import tqdm
import json
import os
from gatherImagesFunctions import *
from gatherMetadataFunctions import *
from htmldate import find_date
from newspaper import Article
import langid
import concurrent.futures


base_path = os.getcwd()
name_folder = "image_ks_"

urls = []
for n in range(1,5):
    list_url = gatherPagesUrlsFolder(os.path.join(base_path, name_folder + str(n)))
    urls = urls + list_url
urls = list(set(urls))
urls = random.sample(urls,10)
print("{} urls gathered in all folders".format(len(urls)))

html_destination = os.path.join(base_path,name_folder,'html')
if not os.path.exists(html_destination):
    os.makedirs(html_destination)

# Scrape Images
print(' --Scraping {} .htmls to {}'.format(len(urls), html_destination))
#scraperOne(all_url, images_destination)

os.chdir(html_destination)
with concurrent.futures.ThreadPoolExecutor() as e:
    for u in tqdm(urls):
        e.submit(gatherHtml, u)
os.chdir(os.path.join(base_path))
