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
from gatherImagesFunctions import *
from htmldate import find_date

base_path = os.getcwd()

def gatherImagessUrls(name, n_folders) :
    base_path = os.getcwd()
    all_url = []
    for n in range(1,n_folders+1):
        folder_path = name + str(n)
        folder_path = os.path.join(base_path, folder_path)
        print(folder_path)
        if os.path.isdir(folder_path):
            list_json = [j for j in os.listdir(folder_path) if ".json" in j]
        if os.path.isdir(os.path.join(folder_path,"img")):
            list_imgs = [i for i in os.listdir(os.path.join(folder_path,"img"))]

        for js in list_json:
            json_data = loadJson(os.path.join(folder_path,js))
            try:
                temp_url = getImageURL(json_data)
                all_url = all_url + temp_url
            except KeyError:
                print('corrupted json file, probably an 400 Error!')
                continue
    return all_url

def gatherPagesUrls(name, n_folders) :
    base_path = os.getcwd()
    all_url = []
    for n in range(1,n_folders+1):
        folder_path = name + str(n)
        folder_path = os.path.join(base_path, folder_path)
        print(folder_path)
        if os.path.isdir(folder_path):
            list_json = [j for j in os.listdir(folder_path) if ".json" in j]
        if os.path.isdir(os.path.join(folder_path,"img")):
            list_imgs = [i for i in os.listdir(os.path.join(folder_path,"img"))]

        for js in list_json:
            json_data = loadJson(os.path.join(folder_path,js))
            try:
                temp_url = getPages(json_data)
                all_url = all_url + temp_url
            except KeyError:
                print('corrupted json file, probably an 400 Error!')
                continue
    return all_url

def gatherDates(list_urls):
    url_d = dict()
    for i in list_urls:
        #print(i)
        d = find_date(i)
        url_d.update({i:d})
    return url_d

l = gatherPagesUrls("image_ks_",2)

l = l[0:40]
d = gatherDates(l)

for x,z in d.items():
    print(z)
