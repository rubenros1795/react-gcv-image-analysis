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
import uuid
import shutil
from PIL import Image
import io

def loadJson(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
        return data


def getImageURL(json_object):
    list_url = []

    for c,i in enumerate(json_object['responses'][0]['webDetection']['pagesWithMatchingImages']):
        if 'partialMatchingImages' in i.keys():

            for c2,x in enumerate(i['partialMatchingImages']):
                for u in list(dict(x).values()):
                    list_url.append(u)

        if 'fullMatchingImages' in i.keys():

            for c2,x in enumerate(i['fullMatchingImages']):
                for u in list(dict(x).values()):
                    list_url.append(u)
    return list_url

def scraperOne(list_url,destination_path):
    print('(scraper called with {} images)'.format(len(list_url)))
    headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}
    for c,url in enumerate(list_url):
        fn = c
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
            continue

        try:
            fn = os.path.join(destination_path,fn)
            #urllib.request.urlretrieve(url, fn)
            resp = requests.get(url, headers=headers).content
            with open(fn, "wb") as f:
                f.write(resp)

        except Exception as e:
        #except (HTTPError, URLError, TimeoutError,IncompleteRead, ConnectionError) as e:
            print(e)
            continue

def scraperTwo(url):
    fn = uuid.uuid1()

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
        return 0

    try:
        image_content = requests.get(url, timeout=20).content

    except Exception as e:
        with open(fn[:-4] + ".txt",'w') as f:
            f.write("ERROR: " + str(e) + "|" + url)
        return

    try:
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        with open(fn, 'wb') as f:
            image.save(f)
        with open(fn[:-4] + ".txt",'w') as f:
            f.write("SUCCESS: " + url)
        del image

    except Exception as e:
        with open(fn[:-4] + ".txt",'w') as f:
            f.write("ERROR: " + str(e) + "|" + url)
        return

