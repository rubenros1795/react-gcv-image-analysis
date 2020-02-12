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
from newspaper import Article

url = 'https://turnupthevolume.blog/2019/05/04/history-4-may-1970-kent-state-shootings-in-ohio/'
article = Article(url)
article.download()
article.parse()
print(article.text)
