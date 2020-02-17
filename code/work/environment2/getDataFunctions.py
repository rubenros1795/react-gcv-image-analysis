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
from getImagesFunctions import *
from htmldate import find_date
from newspaper import Article

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
    print("Initating gatherPagesUrls")
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
    print('finished gatherPagesUrls')
    return all_url

def gatherPagesUrlsFolder(folder_path) :
    if os.path.isdir(folder_path):
        list_json = [j for j in os.listdir(folder_path) if ".json" in j]
    if os.path.isdir(os.path.join(folder_path,"img")):
        list_imgs = [i for i in os.listdir(os.path.join(folder_path,"img"))]

    all_url = []
    for js in list_json:
        json_data = loadJson(os.path.join(folder_path,js))
        try:
            temp_url = getPages(json_data)
            all_url = all_url + temp_url
        except KeyError:
            print('corrupted json file, probably an 400 Error!')
            continue
    print('finished gatherPagesUrlsFolder')
    return all_url

def gatherDates(list_urls):
    url_d = dict()
    for i in list_urls:
        #print(i)
        try:
            d = find_date(i)
            url_d.update({i:d})
        except Exception as e:
            print(e)
            continue
    return url_d

def gatherSingleDate(url):
    try:
        d = find_date(url)

    except Exception as e:
        print(e)
        return

    return {url:d}

def gatherFullText(url):
    article = Article(url)
    article.download()
    article.parse()
    txt = article.text
    txt = txt.replace('\n\n', '\n')
    return txt

def gatherHtml(url):
    fn = regexz.sub(r'\W+', '', url)
    fn = fn + ".html"

    try:
        #urllib.request.urlretrieve(url, fn)
        with open(fn, "w") as file:
            file.write(str(soup))
    except Exception as e:
        #except (HTTPError, URLError, TimeoutError,IncompleteRead, ConnectionError) as e:
        print(e)
        return 0
