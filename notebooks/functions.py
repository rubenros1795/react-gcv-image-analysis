import urllib.request, urllib.error, urllib.parse
from urllib.error import HTTPError, URLError
from boilerpipe.extract import Extractor
from nltk.tokenize import word_tokenize
from urllib.parse import urlparse
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
import codecs
import datetime
import requests
import os.path
import string
import random
import shutil
import json
import math
import time
import nltk
import glob
import uuid
import csv
import io




import langid
from langid.langid import LanguageIdentifier, model
identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)


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


class Organize():
    def __init__(self,folder_base="",num_iterations=0,iteration=0):
        self.folder_base = folder_base
        self.num_iterations = num_iterations
        self.iteration = iteration

    def gatherJson(folder_base,iteration):
        folder_path = folder_base + "_" + str(iteration)
        folder_path = os.path.join(folder_path)

        list_json = [j for j in os.listdir(folder_path) if ".json" in j]

        results = []
        for fn in list_json:
            with open(os.path.join(folder_path, fn)) as jsf:
                #print(folder_path, fn)
                data = json.load(jsf)
                try:
                    data = data['responses'][0]['webDetection']['pagesWithMatchingImages']
                    for d in data:
                        results.append(d)
                except KeyError:
                    print('{} has an error'.format(fn))
        return results

    def gatherImageUrlsProcessed(folder_base, iteration) :
        base_path = os.getcwd()
        folder = os.path.join(base_path, folder_base + "_" + str(iteration), "img")
        if not os.path.exists(folder):
            print('No images found in {}: path does not yet exist'.format(folder_base + "_" + str(iteration) + "/img"))
            return
        else:
            list_txt = [i for i in os.listdir(folder) if ".txt" in i]
            list_txt = [os.path.join(folder,i) for i in list_txt]

            success = 0
            errors = 0

            if len(list_txt) == 0:
                print('No images found in {}: no images in folder'.format(folder_base + "_" + str(iteration) + "/img"))
            else:
                list_url = []
                for t in list_txt:
                    with open(t,'r') as f:
                        c = f.readlines()
                    if c[0][:5] == "ERROR":
                        errors += 1
                        list_url.append(c[0])
                    else:
                        success += 1
                        list_url.append(c[0])
                print("Found {} successful and {} failed scraped images".format(success, errors))
                return list_url

class WebPage():
    def __init__(self,url,list_url,filename):
        self.url = url
        self.list_url = list_url
        self.filename = filename

    def gatherDateMatch(url):
        poss_years = [str(i) for i in range(1990,2021)]
        poss_months_char = {"jan":'01', "feb":'02', "mar":'03', "apr":'04', "may":'05', "jun":'06', "jul":'07', "aug":'08',"sep":'09', "oct":'10', "nov":'11', "dec":'12'}
        poss_months_int = "01 02 03 04 05 06 07 08 09 10 11 12"
        poss_days_int = [str(i) for i in range(1,32)]
        poss_days_int = ["0"+i for i in poss_days_int if len(i) == 1] + [i for i in poss_days_int if len(i) > 1]

        u = url.split('/')
        doubts = "no"
        year = "na"
        month = 'na'
        day = 'na'

        if any(y in u for y in poss_years):
            index_year = u.index([y for y in u if y in poss_years][0])

            # IF MONTH IS A STRING: "JAN" OR "OCT"
            if u[index_year+1] and u[index_year+1] in poss_months_char.keys():
                year = u[index_year]
                month = poss_months_char[u[index_year+1]]
                if u[index_year+2] and u[index_year+2] in poss_days_int:
                    day = u[index_year+2]
                    status = "found something"
                if u[index_year+2] and u[index_year+2] not in poss_days_int:
                    day = "na"


            # IF PATTERN IS YEAR-MONTH-DAY
            try:
                if u[index_year+1] in poss_months_int and u[index_year+2] in poss_days_int:
                    year = u[index_year]
                    month = u[index_year+1]
                    day = u[index_year+2]
                    status = "found something"
                    if u[index_year+2] in poss_months_int and u[index_year+1] in poss_days_int and u[index_year+1] != u[index_year+2]:
                        doubts = "yes"
            except IndexError:
                doubts = "yes"


            # IF PATTERN IS YEAR-DAY-MONTH
            try:
                if u[index_year+1] in poss_days_int and u[index_year+2] in poss_months_int:
                    year = u[index_year]
                    month = u[index_year+2]
                    day = u[index_year+1]
                    status = "found something"
                    if u[index_year+1] in poss_months_int and u[index_year+2] in poss_days_int and u[index_year+2] != u[index_year+1]:
                            doubts = "yes"
            except IndexError:
                    doubts = "yes"

            # IF PATTERN IS MONTH-DAY-YEAR
            try:
                if u[index_year-1] in poss_days_int and u[index_year-2] in poss_months_int:
                    year = u[index_year]
                    month = u[index_year-2]
                    day = u[index_year-1]
                    status = "found something"
                    if u[index_year-1] in poss_months_int and u[index_year-2] in poss_days_int and u[index_year-1] != u[index_year-2]:
                        doubts = "yes"
            except IndexError:
                    doubts = "yes"

            # IF PATTERN IS DAY-MONTH-YEAR
            try:
                if u[index_year-2] in poss_days_int and u[index_year-1] in poss_months_int:
                    year = u[index_year]
                    month = u[index_year-1]
                    day = u[index_year-2]
                    status = "found something"
                    if u[index_year-2] in poss_months_int and u[index_year-1] in poss_days_int and u[index_year-2] != u[index_year-1]:
                        doubts = "yes"
            except IndexError:
                    doubts = "yes"

            status = "found something"

            if doubts == "no" and status == "found something" and year != "na" and month != "na" and day != "na":
                #return [year,month,day]
                return "-".join([year,month,day])

            elif doubts == "yes":
                #return ["na"]
                return "na"
        else:
            #status = "found nothing"
            return "na"

    def gatherSingleDate(url):
        date = WebPage.gatherDateMatch(url)
        if date == "na":
            try:
                date = find_date(url)
                return date
            except Exception as e:
                print(e)
                date = "ERROR:{}".format(e)
                return date
        else:
            return date

    def gatherSingleDateMultiProc(url,filename):
        date = WebPage.gatherDateMatch(url)
        if date == "na":
            try:
                date = find_date(url)
                if date is None:
                    date = "na"
                with open(filename, 'a') as f:
                    f.write(url+'|'+date+"\n")
            except Exception as e:
                print(e)
                date = "ERROR:{}".format(e)
                if date is None:
                    date = "na"
                with open(filename, 'a') as f:
                    f.write(url+'|'+date+"\n")
        elif date is None:
            with open(filename, 'a') as f:
                f.write(url+'|'+"na"+"\n")
        else:
            with open(filename, 'a') as f:
                f.write(url+'|'+date+"\n")

    def gatherListDates(list_urls):
        url_d = dict()
        for u in list_urls:
            date = Date.gatherSingleDate(u)
            url_d.update({u:date})
        return url_d

    def PoolScrapeDate(list_url, destination_path,filename):
        threads = min(30, len(list_url))

        # We can use a with statement to ensure threads are cleaned up promptly
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            # Start the load operations and mark each future with its URL
            future_to_url = {executor.submit(WebPage.gatherSingleDateMultiProc, url, filename): url for url in list_url}
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    data = future.result()
                except Exception as exc:
                    pass
                    #print('%r generated an exception: %s' % (url, exc))
                else:
                    pass

class HTML():
    def __init__(self,destination_path, list_url,filename):
        self.destination_path = destination_path
        self.list_url = list_url
        self.filename = filename

    def Scraper(url, destination_path):
        title = os.path.join(destination_path, str(uuid.uuid4()) + '.html')
        resp = requests.get(url, verify=False, timeout=30)

        with open(title, "wb") as fh:
            fh.write(resp.content)

        with open(os.path.join(destination_path,"results.txt"), "a") as fh:
            fh.write("{}|{}{}".format(title[:-5], url, '\n'))

        time.sleep(0.1)

    def PoolScrape(list_url, destination_path):
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)

        threads = min(30, len(list_url))
        # We can use a with statement to ensure threads are cleaned up promptly
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            # Start the load operations and mark each future with its URL
            future_to_url = {executor.submit(HTML.Scraper, url, destination_path): url for url in list_url}
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    data = future.result()
                except Exception as exc:
                    pass
                    #print('%r generated an exception: %s' % (url, exc))
                else:
                    pass

class ParseText():
    def __init__(self,html_folder):
        self.html_folder = html_folder

    def Import(html_folder):

        print("Looking for results.txt in {}".format(html_folder))
        with open(os.path.join(html_folder, "results.txt")) as f:
            urls = f.readlines()
            urls_new = []
            for u in urls:
                try:
                    id = str(u).split('|')[0]
                    url = str(u).split('|')[1].replace('\n','')
                    id = id + '.html'
                    id = os.path.join(html_folder,id)
                    urls_new.append((id, url))
                except IndexError:
                    print('error in loading url')
                    continue

        return urls_new


    def ParserBoilerArticle(html_object):
        extractor = Extractor(extractor='ArticleSentencesExtractor', html=html_object)
        sents = extractor.getText()
        try:
            sents = list(nltk.sent_tokenize(sents))
            return sents
        except Exception as e:
            print(e)
            return


    def ParserBoilerDefault(html_object):
        extractor = Extractor(extractor='DefaultExtractor', html=html_object)
        sents = extractor.getText()
        try:
            sents = list(nltk.sent_tokenize(sents))
            return sents
        except Exception as e:
            return

    def ParserBoilerEverything(html_object):
        extractor = Extractor(extractor='DefaultExtractor', html=html_object)
        sents = extractor.getText()
        try:
            sents = list(nltk.sent_tokenize(sents))
            return sents
        except Exception as e:
            return

    def ParserRaw(html_object):
        soup = BeautifulSoup(html_object, "html.parser")
        [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
        text = soup.getText()
        #text = [t for t in text if t]
        return text

    def Parse(html_folder):
        urls = ParseText.Import(html_folder)
        errors = 0
        print("INFO: parsing tekst from {} files".format(len(urls)))
        destination_path = os.path.join(html_folder[:-4], "txt")

        if not os.path.exists(destination_path):
            os.makedirs(destination_path)

        text_dict = dict()
        for u in tqdm(urls):
            fn = os.path.join(html_folder, u[0])
            url = u[1]
            id = "_".join([fn,url])
            try:
                with codecs.open(fn,'r',encoding='utf-8',errors='ignore') as f:
                    html_object = f.read()

                sents = ParseText.ParserBoilerArticle(html_object)

                if len(sents) < 2 or sents is None:
                    sents = ParseText.ParserBoilerDefault(html_object)
                if len(sents) < 2 or sents is None:
                    sents = ParseText.ParserBoilerEverything(html_object)
                if len(sents) < 2 or sents is None:
                    sents = ParseText.ParserRaw(html_object)

                if type(sents) == list:
                    text_dict.update({id:[str(sent) for sent in sents]})
                if type(sents) == str:
                    text_dict.update({id:[sents]})

            except Exception as e:
                print(e)
                continue

        with open(os.path.join(destination_path, "parsed_text.json"), "w") as js:
            json.dump(text_dict,js)

class Language():
    def __init__(self,url,text):
        self.text = text
        self.url = url

    def ParseUrl(url):
        delimiters = "/", ".", " "
        regexPattern = '|'.join(map(regexz.escape, delimiters))
        url_phrase = [x for x in urlparse(url) if x][2:]
        url_phrase = " ".join([x for x in url_phrase if x])
        url_phrase = regexz.split(regexPattern, url_phrase)
        url_phrase = [x for x in url_phrase if x]

        if len(url_phrase) == 0:
            return

        url_phrase = max(url_phrase, key=len)

        if "-" in url_phrase:
            url_phrase = url_phrase.split('-')

        lang = identifier.classify(" ".join(url_phrase))
        if lang is not None:
            return [lang[0],lang[1]]
        else:
            return

    def ParseText(text):
        try:
            lang = identifier.classify(str(text[1:-1]))
            return [lang[0],lang[1]]
        except Exception as e:
            return ["na","na"]

class IM():
    def __init__(url,filename):
        self.url = url
        self.filename = filename

    def scraperTwo(url):
        fn = uuid.uuid1()
        #fn = regexz.sub(r'\W+', '', url)

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

        #try:
            #image_content = requests.get(url, timeout=20).content

        #except Exception as e:
            #with open(fn[:-4] + ".txt",'w') as f:
            #    f.write("ERROR: " + str(e) + "|" + url)
            #return

        try:
            image_content = requests.get(url, timeout=20,stream=True).content
            image_file = io.BytesIO(image_content)
            image = Image.open(image_file).convert('RGB')
            with open(fn, 'wb') as f:
                image.save(f)
            with open(fn[:-4] + ".txt",'w',encoding='utf-8') as f:
                f.write("SUCCESS: " + url)
            del image

        except Exception as e:
            with open(fn[:-4] + ".txt",'w') as f:
                f.write("ERROR: " + str(e) + "|" + url)
            return

    def imgTag(filename):
        extensions = ".jpg .JPG .JPEG .jpeg .Jpeg .png".split(' ')

        #try:
            #content = requests.get(url,t).content
        #except Exception as e:
            #print(e)
            #return
        #soup = BeautifulSoup(content,'lxml')

        with codecs.open(filename,'r',encoding='utf-8',errors='ignore') as f:
            html_object = f.read()
        soup = BeautifulSoup(html_object, "html.parser")
        image_tags = []
        for tag in ['img','meta','a']:
            tt = soup.findAll(tag)
            image_tags = image_tags + tt
        list_url = []
        for c,tag in enumerate(image_tags):
            attributes = dict(tag.attrs)

            for k,v in attributes.items():
                # Extract Image
                if any(substring in v for substring in extensions):
                    list_url.append(v)

        if len(list_url) > 0:
            return list_url
        else:
            return
