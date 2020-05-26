import json
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib
from tqdm import tqdm
import operator
import seaborn as sns
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
import re,string
from nltk.tokenize import sent_tokenize
import spacy
import networkx as nx
from nltk.corpus import stopwords
from spacy import displacy
import pandas as pd
import nltk
import math,re

spacy_d = {"it":"it_core_news_sm",
           "es":"es_core_news_sm",
           "en":"en_core_web_sm",
           "nl":"nl_core_news_sm"}

data = pd.read_csv(open('/media/ruben/FEF44259F44213F5/Users/Ruben/Documents/GitHub/ReACT_GCV/data/images_tables_article_carlo/data-full-dd-full.csv'),engine='c')
data['sentences'] = [" ".join(str(x).split('||')).replace('||',' ') for x in list(data['sentences'])]

def NounAdjPairs(language,keyword_vocab, verbose=True, export=True,fn="",extension_dict={}):
    nlp = spacy.load(spacy_d[language])
    ss=[]

    for c,i in enumerate(data['sentences']):
        i = replaceExtension(i,extension_dict)

        if any(w in str(i) for w in keyword_vocab) and data['language'][c] == language:
            sentences = sent_tokenize(i)
            sentences = [s for s in sentences if any(n in s for n in keyword_vocab)]

            for sentence in sentences:
                doc = nlp(sentence)
                for i in doc:
                    if i.pos_ in ["NOUN", "PROPN"] and str(i.text) in keyword_vocab:
                        comps = [j for j in i.children if j.pos_ in ["ADJ"]]
                        if comps:
                            for co in comps:
                                print("head: {} | child: {} | dep: {}".format(i.text,co.text,co.dep_))
                                ss.append([str(co),str(i),str(i.dep_),data['identifier'][c]])

    ss = pd.DataFrame(ss,columns=['adj','noun','dep','id'])

    if verbose==True:
        counts = Counter(list(ss['adj'].astype(str))).most_common(25)
        [print(x[0],": ",x[1]) for x in counts]

    ss.to_csv('/media/ruben/FEF44259F44213F5/Users/Ruben/Documents/GitHub/ReACT_GCV/data/images_tables_article_carlo/pos-analysis/{}'.format(fn),index=False)
    Transform2Counts('/media/ruben/FEF44259F44213F5/Users/Ruben/Documents/GitHub/ReACT_GCV/data/images_tables_article_carlo/pos-analysis/{}'.format(fn), type_a="NAP")
    return

def AdjNounPairs(language,keyword_vocab, verbose=True, export=True,fn=""):
    nlp = spacy.load(spacy_d[language])
    ss=[]

    for c,i in enumerate(data['sentences']):

        if any(w in str(i) for w in keyword_vocab) and data['language'][c] == language:
            sentences = sent_tokenize(i)
            sentences = [s for s in sentences if any(n in s for n in keyword_vocab)]

            for sentence in sentences:
                doc = nlp(sentence)
                for i in doc:
                    if i.pos_ in ["VERB", "NOUN"]:
                        comps = [j for j in i.children if j.pos_ in ['ADJ',"ADP"] and str(j.text) in keyword_vocab]
                        if comps:
                            for co in comps:
                                ss.append([str(co),str(i),str(co.dep_),data['identifier'][c]])
    ss = pd.DataFrame(ss,columns=['adjective_adverb','modified_verb_noun','dep','id'])

    counts = Counter(list(ss['modified_verb_noun'].astype(str))).most_common(25)
    [print(x[0],": ",x[1]) for x in counts]
    ss.to_csv('/media/ruben/FEF44259F44213F5/Users/Ruben/Documents/GitHub/ReACT_GCV/data/images_tables_article_carlo/{}'.format(fn),index=False)
    return


def NounVerbPairs(language,keyword_vocab, verbose=True, export=True,fn="",extension_dict={},lemmatize=True):
    nlp = spacy.load(spacy_d[language])
    for c,i in enumerate(data['sentences']):
        i = replaceExtension(i,extension_dict)

        if any(w in str(i) for w in keyword_vocab) and data['language'][c] == language:
            sentences = sent_tokenize(i)
            sentences = [s for s in sentences if any(n in s for n in keyword_vocab)]

            for sentence in sentences:
                doc = nlp(sentence)
                for i in doc:
                    if i.pos_ in ["NOUN", "PROPN"] and str(i.text) in keyword_vocab:
                        comps = [j for j in i.children if j.pos_ in ["VERB"]]
                        if comps:
                            for verb in comps:
                                print("noun: {} | verb_lemma: {} | dep: {}".format(i.text,verb.lemma_,verb.dep_))
                                ss.append([str(verb.text),str(verb.lemma_),str(i),str(i.dep_),data['identifier'][c]])

    ss = pd.DataFrame(ss,columns=['verb','verb_lemma','noun','dep','id'])

    if verbose==True:
        counts = Counter(list(ss['verb_lemma'].astype(str))).most_common(25)
        [print(x[0],": ",x[1]) for x in counts]

    ss.to_csv('/media/ruben/FEF44259F44213F5/Users/Ruben/Documents/GitHub/ReACT_GCV/data/images_tables_article_carlo/pos-analysis/{}'.format(fn),index=False)
    Transform2Counts('/media/ruben/FEF44259F44213F5/Users/Ruben/Documents/GitHub/ReACT_GCV/data/images_tables_article_carlo/pos-analysis/{}'.format(fn), type_a="NVP")
    return

def Transform2Counts(path,type_a=''):
    df = pd.read_csv(path)
    df['n'] = 1

    if type_a == "NAP": # for types see functions above
        df = df[['adj','noun','n']]
        df = df.groupby(['adj','noun']).sum().reset_index()
    if type_a == "ANP":
        df = df[['adjective_adverb','modified_verb_noun','n']]
        df = df.groupby(['adjective_adverb','modified_verb_noun']).sum().reset_index()
    if type_a == "NVP":
        df = df[['verb_lemma','noun','n']]
        df = df.groupby(['verb_lemma','noun']).sum().reset_index()

    fn = path.replace('.csv','')
    fn = fn + "-counts.csv"
    df.to_csv(fn,index=False)

def replaceExtension(doc_, extension_dict={}):
    for k,v in extension_dict.items():
        for i in v:
            doc_ = doc_.replace(i,k)
    return doc_

def PMI(keywords,language,language_code,threshold,extension_dict={}):
    dd = data[data['language'] == language_code]
    stopz = stopwords.words(language)

    # Merge all data to token list and replace specifically set words
    all_docs = [replaceExtension(s,extension_dict) for s in dd['sentences']]
    print("Number of Webpages: {}".format(len(all_docs)))

    # Make a Subset of words that appear in the sentence_context of keyword

    target_word_dict = dict()

    for kw in keywords:
        ss_docs = [s.split(' ') for s in all_docs if kw in s]
        target_words = [re.sub('[\W_]+', '', str(item)) for sublist in ss_docs for item in sublist if len(item) > 2]
        counts_target_words = dict(Counter(target_words))
        target_words = list(set([w for w in target_words if counts_target_words[w] > threshold and w not in stopz]))
        target_word_dict.update({kw:target_words})
        print("Number of TargetWords for {}: {}".format(kw,len(target_words)))

    sentences = [nltk.sent_tokenize(d) for d in all_docs]
    sentences = [item for sublist in sentences for item in sublist]
    print("Number of Sentences: {}".format(len(sentences)))

    # Get PMI values
    for kw in keywords:
        pmi_d = []
        p_keyword = len([s for s in sentences if kw in s.split(' ')]) / len(sentences) * 100

        for w in target_word_dict[kw]:
            ntarget = len([s for s in sentences if w in s.split(' ')])
            nxy = len([s for s in sentences if w in s and kw in s.split(' ')])

            if ntarget < threshold or nxy < threshold:
                continue

            ptarget = len([s for s in sentences if w in s]) / len(sentences) * 100
            pxy = len([s for s in sentences if w in s and kw in s]) / len(sentences) * 100


            if len([s for s in sentences if w in s and kw in s]) > 0:
                pmi = math.log((pxy) / (ptarget * p_keyword))
                pmi_d.append([w,pmi,ntarget,nxy])
            else:
                continue
        if len(pmi_d) > 0:
            t = pd.DataFrame(pmi_d,columns = ['w','s','ntarget','ntogether'])
            t.to_csv('/media/ruben/FEF44259F44213F5/Users/Ruben/Documents/GitHub/ReACT_GCV/data/images_tables_article_carlo/pmi-{}-en.csv'.format(kw),index=False)
        else:
            print("{} has no PMI candidates that meet the threshold".format(kw))
