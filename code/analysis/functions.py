import urllib.request, urllib.error, urllib.parse
from urllib.error import HTTPError, URLError
from http.client import IncompleteRead
from htmldate import find_date
from bs4 import BeautifulSoup
import concurrent.futures
from tqdm import tqdm
import urllib.request
from PIL import Image
import numpy as np
import urllib.request
import pandas as pd
import re as regexz
import requests
import os.path
import string
import random
import shutil
import json
import glob
import uuid
import io


class Json():
    def __init__(self, filename, list_json):
        self.filename = filename
        self.json_object = json_object
        self.list_json = list_json

    def load(filename):
        with open(filename) as json_file:
            data = json.load(json_file)
            return data

    def extract_images(filename):

        json_object = Json.load(filename)

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

    def extract_image_folder(list_json):
        all_url = []
        for js in list_json:
            try:
                temp_url = Json.extract_images(js)
                all_url = all_url + temp_url
            except KeyError:
                print('corrupted json file, probably an 400 Error!')
                continue
        return list(set(all_url))

class Im():

    def __init__(url,list_url):
        self.url = url
        self.list_url = list_url

    def Scraper(url):
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
            #with open(fn[:-4] + ".txt",'w') as f:
            #    f.write("ERROR: " + str(e) + "|" + url)
            return

    def Scrape(list_url):
        with concurrent.futures.ThreadPoolExecutor() as e:
            for u in list_url:
                e.submit(Im.Scraper, u)

    def RemoveSmall(folder,size=2500):
        list_images = [os.path.join(folder,l) for l in os.listdir(folder) if ".png" in l or ".jpg" in l]
        too_small = [l for l in list_images if int(os.stat(l).st_size) < size]
        too_small = too_small + [l[:-3]+"txt" for l in too_small]
        print('removing {} small images'.format(len(too_small)))
        [os.remove(i) for i in too_small]

class Duplicates():
    def __init__(images_destination):
        self.images_destination = images_destination

    def remove(images_destination):

        list_img = os.listdir(images_destination)
        list_img = [img for img in list_img if ".txt" not in img]

        if len(list_img) > 1:
            df = pd.DataFrame()

            for img in list_img:
                try:
                    im = Image.open(os.path.join(images_destination,img))
                    width, height = im.size
                    im = np.array(im)
                    w,h,d = im.shape
                    im.shape = (w*h, d)
                    values_ = tuple(np.average(im, axis=0))
                    values_ = "_".join([str(int(round(v))) for v in values_])
                    print(width,height,values_,img)
                    tmp = pd.DataFrame([width,height,values_,img]).T
                    tmp.columns = ['w','h','rgb','id']
                    df = df.append(tmp)
                except Exception as e:
                    print(e)
                    pass
            df.columns = ['w','h','rgb','id']
            df['w'] = df['w'].astype(int)
            df['h'] = df['h'].astype(int)
            df['iid'] = df['rgb'].astype(str) + df['w'].astype(str) + df['h'].astype(str)
            dfn = df.drop_duplicates(subset='iid', keep="first")

            print('--- Found {}/{} duplicates'.format(len(df) - len(dfn),len(df)))

            removal_list = [im for im in list(df['id']) if im not in list(dfn['id'])]

            for img in removal_list:
                os.remove(os.path.join(images_destination,img))
                os.remove(os.path.join(images_destination,img[:-3] + "txt"))
        else:
            print("no image files found, no duplicates removed")
