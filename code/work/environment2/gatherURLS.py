from bs4 import BeautifulSoup
import datetime
import pandas as pd
import requests
import string
import re as regexz
import random
import os.path
from tqdm import tqdm
import json
import os
from scrapeImages import *


base_path = os.getcwd()

all_url = []
for i in range(1,5):
    target_folder = "image_ks_" + str(i)
    list_json = [j for j in os.listdir(os.path.join(base_path, target_folder)) if ".json" in j]
    for js in list_json:
        json_data = loadJson(os.path.join(base_path, target_folder,js))

        try:
            temp_url = getImageURL(json_data)
            all_url = all_url + temp_url
        except KeyError:
            print('corrupted json file, probably an 400 Error!')
            continue
print(len(set(all_url)))
