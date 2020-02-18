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
from gatherDataFunctions import *
from htmldate import find_date
from newspaper import Article
import langid
import concurrent.futures



base_path = os.getcwd()
name_folder = "image_ks_"

d_iter_urls = dict()
for n in range(1,2):
    list_url = gatherPagesUrlsFolder(os.path.join(base_path, name_folder + str(n)))
    d_iter_urls.update({n:list_url})
