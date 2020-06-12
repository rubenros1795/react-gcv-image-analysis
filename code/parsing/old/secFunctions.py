from bs4 import BeautifulSoup
import datetime, csv
import pandas as pd
import requests
import string
import re
import random
from tqdm import tqdm
import json
import os
from htmldate import find_date
import time
import uuid
import concurrent.futures
from nltk.tokenize import word_tokenize
import spacy
from boilerpipe.extract import Extractor
import codecs
import math
import shutil
from PIL import Image
import io
from urllib.parse import urlparse
import langid
from langid.langid import LanguageIdentifier, model
identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)


nlp = spacy.load('en_core_web_sm')

class dateparser():
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
        date = dateparser.gatherDateMatch(url)
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
        date = dateparser.gatherDateMatch(url)
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
            future_to_url = {executor.submit(dateparser.gatherSingleDateMultiProc, url, filename): url for url in list_url}
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    data = future.result()
                except Exception as exc:
                    pass
                    #print('%r generated an exception: %s' % (url, exc))
                else:
                    pass

class pagescraper():
    def __init__(self,destination_path, list_url,filename):
        self.destination_path = destination_path
        self.list_url = list_url
        self.filename = filename

    def Scraper(url, destination_path):
        #print('Called')
        title = os.path.join(destination_path, str(uuid.uuid4()) + '.html')
        resp = requests.get(url, verify=False, timeout=30)

        with open(title, "wb") as fh:
            fh.write(resp.content)

        with open(os.path.join(destination_path,"results.txt"), "a") as fh:
            fh.write("{}|{}{}".format(title[:-5], url, '\n'))

        time.sleep(0.1)

    def PoolScrape(list_url, destination_path):
        threads = min(30, len(list_url))

        # We can use a with statement to ensure threads are cleaned up promptly
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            # Start the load operations and mark each future with its URL
            future_to_url = {executor.submit(pagescraper.Scraper, url, destination_path): url for url in list_url}
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    data = future.result()
                except Exception as exc:
                    pass
                    #print('%r generated an exception: %s' % (url, exc))
                else:
                    pass

class textparser():
    def __init__(self,html_folder):
        self.html_folder = html_folder

    def Import(html_folder):

        if os.path.exists(os.path.join(html_folder, "results.txt")):
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
                        continue
                return urls_new
        else:
            print("results.txt not found in {}".format(html_folder))


    def ParserBoilerArticle(html_object):
        extractor = Extractor(extractor='ArticleSentencesExtractor', html=html_object)
        sents = extractor.getText()
        try:
            sents = list(nlp(sents).sents)
            return sents
        except Exception as e:
            return

    def ParserBoilerDefault(html_object):
        extractor = Extractor(extractor='DefaultExtractor', html=html_object)
        sents = extractor.getText()
        try:
            sents = list(nlp(sents).sents)
            return sents
        except Exception as e:
            return

    def ParserBoilerEverything(html_object):
        extractor = Extractor(extractor='DefaultExtractor', html=html_object)
        sents = extractor.getText()
        try:
            sents = list(nlp(sents).sents)
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
        urls = textparser.Import(html_folder)
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

                sents = textparser.ParserBoilerArticle(html_object)

                if len(sents) < 2 or sents is None:
                    sents = textparser.ParserBoilerDefault(html_object)
                if len(sents) < 2 or sents is None:
                    sents = textparser.ParserBoilerEverything(html_object)
                if len(sents) < 2 or sents is None:
                    sents = textparser.ParserRaw(html_object)

                if type(sents) == list:
                    text_dict.update({id:" ".join([str(sent) for sent in sents])})
                if type(sents) == str:
                    text_dict.update({id:sents})

            except Exception as e:
                continue

        with open(os.path.join(destination_path, "parsed_text.json"), "w") as js:
            json.dump(text_dict,js)

class imagescraper():
    def __init__(url,filename):
        self.url = url
        self.filename = filename

    def Scrape(url):
        fn = uuid.uuid1()
        #fn = re.sub(r'\W+', '', url)

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
        print(fn)

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

    def findtags(filename):
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
