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
import time
import uuid
import concurrent.futures
from nltk.tokenize import word_tokenize

class Organize():
    def __init__(self,folder_base="",num_iterations=0,iteration=0):
        self.folder_base = folder_base
        self.num_iterations = num_iterations
        self.iteration = iteration

    def gatherImageUrlsFromJson(folder_base, num_iterations) :
        base_path = os.getcwd()
        all_url = []
        for n in range(1,num_iterations+1):

            folder_path = folder_base + str(n)
            folder_path = os.path.join(folder_path)

            list_json = [j for j in os.listdir(folder_path) if ".json" in j]

            for js in list_json:
                json_data = loadJson(os.path.join(folder_path,js))
                try:
                    temp_url = getImageURL(json_data)
                    all_url = all_url + temp_url
                except KeyError:
                    print('Found a corrupted json file, probably an 400 Error! --  {}'.format(js))
                    continue
        return all_url

    def gatherImageUrlsProcessed(folder_base, iteration) :
        base_path = os.getcwd()
        folder = os.path.join(base_path, folder_base + str(iteration), "img")
        if not os.path.exists(folder):
            print('No images found in {}: path does not yet exist'.format(folder_base + str(iteration) + "/img"))
            return
        else:
            list_txt = [i for i in os.listdir(folder) if ".txt" in i]
            list_txt = [os.path.join(folder,i) for i in list_txt]

            success = 0
            errors = 0

            if len(list_txt) == 0:
                print('No images found in {}: no images in folder'.format(folder_base + str(iteration) + "/img"))
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

    def gatherPagesUrls(folder_base, num_iterations) :

        base_path = os.getcwd()
        all_url = dict()

        for n in range(1,num_iterations+1):
            folder_path = folder_base + str(n)
            folder_path = os.path.join(base_path, folder_path)

            list_json = [j for j in os.listdir(folder_path) if ".json" in j]
            if len(list_json) == 0:
                print("No .json files found here: {}".format(folder_path))

            errors = 0
            for js in list_json:
                json_data = loadJson(os.path.join(folder_path,js))
                try:
                    temp_url = getPages(json_data)
                    all_url.update({n:temp_url})
                except KeyError:
                    errors += 1
                    continue
        print('Finished page url gathering: {} .json file errors'.format(errors))
        return all_url

    def gatherPagesUrlsFolder(folder_base, iteration) :

        base_path = os.getcwd()
        folder_path = os.path.join(base_path, folder_base + str(iteration))

        list_json = [j for j in os.listdir(folder_path) if ".json" in j]

        errors = 0
        all_url = dict()
        for c,js in enumerate(list_json):
            json_data = loadJson(os.path.join(folder_path,js))
            try:
                temp_url = getPages(json_data)
                all_url.update({c:temp_url})
            except KeyError:
                errors += 1
                continue
        print('Finished page url gathering: {} .json file errors'.format(errors))
        all_url = [list(v) for k,v in all_url.items()]
        all_url = [item for sublist in all_url for item in sublist]
        return all_url

class WebPage():
    def __init__(self,url="",list_url=""):
        self.url = url
        self.list_url = list_url

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
            if u[index_year+1] in poss_months_char.keys():
                year = u[index_year]
                month = poss_months_char[u[index_year+1]]
                if u[index_year+2] in poss_days_int:
                    day = u[index_year+2]
                    status = "found something"
                if u[index_year+2] not in poss_days_int:
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
                return [year,month,day]

            elif doubts == "yes":
                #return ["na"]
                return "na"
        else:
            #status = "found nothing"
            return "na"

    def gatherSingleDate(url):
        date = Date.gatherDateMatch(url)
        if date != "na":
            try:
                date = find_date(url)
            except Exception as e:
                print(e)
                date = "ERROR:{}".format(e)

        return date

    def gatherListDates(list_urls):
        url_d = dict()
        for u in list_urls:
            date = Date.gatherSingleDate(u)
            url_d.update({u:date})
        return url_d

class LocalPages():
    def __init__(self,results_file_path, preprocess=True):
        self.results_file = results_file_path
        self.preprocess = True

    def Importer(results_file_path):
        with open(os.path.join(results_file_path, "results.txt")) as f:
            urls = f.readlines()
            urls = [u.split('|') for u in urls]
            urls = [[os.path.join(results_file_path, u[0]) + ".html", u[1].replace('\n','')] for u in urls]
        return urls

    def Parser(results_file_path, preprocess=True):
        urls = LocalPages.Importer(results_file_path)

        d = dict()

        for u in urls:
            fn = u[0]
            url = u[1]

            a = Article(url)

            with open(fn, 'rb') as fh:
                a.html = fh.read()
            a.download_state = 2
            a.parse()
            text = a.text

            if preprocess == True:
                text = text.lower()
                text = text.replace('\n','').split('.')
                text = [word_tokenize(s) for s in text]
                text = [s for s in text if len(s) > 1]

            d.update({fn.split('/')[-1].split('\\')[1] + "_" + url:text})
        d = pd.DataFrame(list(d.items()), columns = ['id', 'text'])

        destination_path = os.path.join(results_file_path[:-4], "txt")
        d.to_csv(os.path.join(destination_path, "parsed_text.csv"),index=False)
        print('CSV saved')

class HTML():
    def __init__(self,destination_path, list_url):
        self.destination_path = destination_path
        self.list_url = list_url

    def Log(destination_path):
        with open("results.txt", 'w') as f:
            f.write('results')

    def Scraper(url):
        title = str(uuid.uuid4()) + '.html'
        resp = requests.get(url, verify=False, timeout=10)

        with open(title, "wb") as fh:
            fh.write(resp.content)

        with open('results.txt', "a") as fh:
            fh.write("{}|{}{}".format(title[:-5], url, '\n'))

        time.sleep(0.1)
