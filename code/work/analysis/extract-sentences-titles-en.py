from functions import *
from random import sample
from htmldate import find_date
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import json
import re, string
import unicodedata
import langid
import operator
from tqdm import tqdm
from gensim.models import Word2Vec
from gensim.models import KeyedVectors

#model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300-SLIM.bin',binary=True)
#model.init_sims(replace=True)

with open('sentences-titles-en.txt','r') as f:
    sentences = f.readlines()

sentences = [s.split(' ') for s in sentences]

sen1 = sentences[0]
print(" ".join(sen1))
d_ = dict()

for s in sentences[0:100]:
    score = model.wmdistance(" ".join(sen1)," ".join(s))
    d_.update({s:score})

print(max(d_.items(), key=operator.itemgetter(1))[0])
