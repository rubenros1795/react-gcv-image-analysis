from bs4 import BeautifulSoup
import datetime
import pandas as pd
import requests
from collections import Counter
import string
import re as regexz
import random
import os.path
from tqdm import tqdm
import json
import os
from gatherImagesFunctions import *
from gatherMetadataFunctions import *
from htmldate import find_date
from newspaper import Article
import langid
import concurrent.futures



base_path = os.getcwd()
name_folder = "image_ks_"

d_iter_urls = dict()
for n in range(1,2):
    list_url = gatherPagesUrlsFolder(os.path.join(base_path, name_folder + str(n)))
    d_iter_urls.update({n:list_url})

#df = pd.DataFrame()
for k,v in d_iter_urls.items():
    v = list(set(v))
    print('iteration {}: {} items'.format(k,len(v)))
    tmp = dict()
    with concurrent.futures.ThreadPoolExecutor() as e:
        for u in v:
            res = e.submit(gatherSingleDate, u)
            res = res.result()
            print(res)
            tmp.update(res)
    #tmp = gatherDates(v)
    tmp = pd.DataFrame(list(tmp.items()),columns=['url','date'])
    tmp['iter'] = k
    fn = "dates_iteration" + str(k) + '.csv'
    tmp.to_csv(fn,index=False)
    print("iteration {} finished".format(k))
