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
import urllib.request, urllib.error, urllib.parse
from urllib.error import HTTPError, URLError
from htmldate import find_date
import glob
import urllib.request
from collections import Counter
import random
from http.client import IncompleteRead

def loadJson(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
        return data

def getPages(json_object):
    list_url = [l['url'] for l in json_object['responses'][0]['webDetection']['pagesWithMatchingImages']]
    return list_url

def getImageURL(json_object):
    list_url = []

    for c,i in enumerate(json_object['responses'][0]['webDetection']['pagesWithMatchingImages']):
        if 'partialMatchingImages' in i.keys():

            for c2,x in enumerate(i['partialMatchingImages']):
                for u in list(dict(x).values()):
                    list_url.append(u)

        elif 'fullMatchingImages' in i.keys():

            for c2,x in enumerate(i['fullMatchingImages']):
                for u in list(dict(x).values()):
                    list_url.append(u)
    return list_url

def scrapeImage(url,savepath):
    fn = savepath
    if "png" in url:
        fn = str(fn) + ".png"
    elif "jpg" in url:
        fn = str(fn) + ".jpg"
    elif "Jpeg" in url:
        fn = str(fn) + ".jpg"
    elif "jpeg" in url:
        fn = str(fn) + ".jpg"
    elif "JPG" in url:
        fn = str(fn) + ".jpg"
    else:
        return e

    try:
        urllib.request.urlretrieve(url, fn)
        print(fn, url)
    except (HTTPError, URLError, TimeoutError,IncompleteRead) as e:
        return e

def getDate(list_urls):
    url_d = dict()
    for i in url_list:
        print(i)
        d = find_date(i)
        url_d.update({i:d})
    return url_d
