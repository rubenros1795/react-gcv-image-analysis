from functions import *
from random import sample
import json
from langid.langid import LanguageIdentifier, model
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib
from tqdm import tqdm
import operator
import matplotlib.pyplot as plt
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
import random
import re
import langid
import spacy

## Load
base_path = "/media/ruben/Data Drive/react-data/protest/{}".format("selection")
model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300-SLIM.bin',binary=True)
model.init_sims(replace=True)

nlp = spacy.load('en_core_web_sm')

## Create Vocabs
def DefVocab(list_words):
    vc = []

    for w in list_words:
        t = [w.lower() for w,s in model.most_similar([w],topn=500) if s > 0.5]
        vc += t
    return list(set(vc))

trans_vocab = DefVocab(['international','global','worldwide','transnational'])
protest_vocab = DefVocab(['protest','demonstration'])

# Get Publication Dates

dates_ref = dict()

for photo in [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]:
    photo_folder = os.path.join(base_path, photo)
    with open(os.path.join(photo_folder,"dates.txt"),'r') as f:
        x = f.readlines()
    dates_ref.update({d.split('|')[0]:d.split('|')[-1].replace('\n','') for d in x if d.split('|')[-1].replace('\n','') != "na" and "ERROR" not in d.split('|')[-1].replace('\n','')})


## Import Sentences
dt = dict()

for photo in [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]:
    photo_folder = os.path.join(base_path, photo)
    num_iterations = [fol for fol in os.listdir(photo_folder) if os.path.isdir(os.path.join(photo_folder,fol)) and "source" not in fol and "context" not in fol]
    num_iterations = len(num_iterations)

    start_iter = 1
    range_iter = [str(i) for i in list(range(1,num_iterations + 1))]

    folder_base = os.path.join(base_path,photo,photo)

    for iteration in range_iter:
        fn = os.path.join(folder_base + "_" +str(iteration),"txt", "parsed_text.json")
        with open(fn) as fp:
            pages = json.load(fp)
        for identifier,sentences in pages.items():
            dt.update({identifier:dict()})
            sentences = [s.replace("\n","").lower() for s in sentences]
            sentences = [re.sub(' +', ' ', s) for s in sentences]

            url = identifier.split('html_')[-1]
            id_ = identifier.split('/html/')[1].split('.html_')[0]
            if url in dates_ref.keys():
                date = dates_ref[url]
            else:
                date = "na"

            dt[identifier].update({"url":url,"identifier":id_,"date":date,"sentences":sentences,"language":langid.classify(" ".join(sentences))[0]})


# Change to Diachronic Data
d_ = dict()

for year in range(2003,2019):
    tmp = {}
    for id_,items1 in dt.items():
        if items1["date"][0:4] == str(year):
            tmp.update({id_:items1})
    d_.update({year:tmp})

# Check Adjectives

candidate = []
for year,items1 in d_.items():
    #vocab_count.update({year:0})
    #total_tokens = [[w for w in " ".join(items1['sentences']).split(' ')] for id_,items1 in d_[year].items()]
    #total_tokens = len([document for sublist in total_tokens for document in sublist])


    for id_,items2 in items1.items():

        sentences = " ".join(items2['sentences']).split(' ')
        indices = [(i,c) for c,i in enumerate(sentences) if i in protest_vocab]

        for i,c in indices:
            try:
                doc = nlp(sentences[c-1])
                pos = ([token.pos_ for token in doc][0])
                if str(pos) == "ADJ":
                    candidate.append(str(year) + "||" + sentences[c-1])
            except Exception as e:
                continue

with open('candidate-adjectives.txt','w') as f:
    for i in candidate:
        f.write(i + " \n")
