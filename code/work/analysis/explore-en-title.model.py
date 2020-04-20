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
import random

model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300-SLIM.bin',binary=True)
model.init_sims(replace=True)

with open('sentences-titles-en.txt','r') as f:
    sentences = f.readlines()

vocab = list(model.wv.vocab)

sentences = [s.replace('\n','').split(' ') for s in sentences]
sentences = [s for s in tqdm(sentences) if len([w for w in s if w in vocab]) > 5]
print('number of sentences: {}'.format(len(sentences)))

sentences = random.sample(sentences, 1000)
sen1 = sentences[0]
d_ = dict()

for s in sentences:
    score = model.wmdistance(" ".join(sen1)," ".join(s))
    d_.update({" ".join(s):score})

print(" ".join(sen1))
print(max(d_.items(), key=operator.itemgetter(1))[0])
