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
html_folder = os.path.join(base_path, "image_ks_", "html")
htmls = os.listdir(html_folder)

soup = BeautifulSoup(open(os.path.join(html_folder, htmls[0])), "html.parser")
imgs = soup.findAll( "img" )
if imgs:
    print(imgs)
