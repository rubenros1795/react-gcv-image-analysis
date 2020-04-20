from bs4 import BeautifulSoup
import datetime, csv
import pandas as pd
import requests
import string
import re as regexz
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

    def Log(destination_path, filename):
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)
        try:
            open(os.path.join(destination_path, filename), 'x').close()
        except FileExistsError:
           pass

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
                    continue

        return urls_new


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
                continue

        with open(os.path.join(destination_path, "parsed_text.json"), "w") as js:
            json.dump(text_dict,js)

        # with open(os.path.join(destination_path, "parsed_text.csv"), "w",encoding='utf-8') as csvFile:
        #     fieldnames = ['id','text']
        #     writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
        #     writer.writeheader()
        #
        #     for u in tqdm(urls):
        #         fn = os.path.join(html_folder, u[0])
        #         url = u[1]
        #         try:
        #             with codecs.open(fn,'r',encoding='utf-8',errors='ignore') as f:
        #                 html_object = f.read()
        #
        #             sents = ParseText.ParserBoilerArticle(html_object)
        #             if len(sents) < 2 or sents is None:
        #                 sents = ParseText.ParserBoilerDefault(html_object)
        #             if len(sents) < 2 or sents is None:
        #                 sents = ParseText.ParserBoilerEverything(html_object)
        #             if len(sents) < 2 or sents is None:
        #                 sents = ParseText.ParserRaw(html_object)
        #             writer.writerow({'id': fn + "_" + url, 'text': sents})
        #         except Exception as e:
        #             errors += 1
        #             print(e)
        #

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
