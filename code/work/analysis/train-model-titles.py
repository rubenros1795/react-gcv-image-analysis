from functions import *
from random import sample
from htmldate import find_date
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import json
import re, string
import unicodedata
import langid
from tqdm import tqdm

base_path = "/media/ruben/Data Drive/react-data/protest/{}".format("selection")

titlesm = dict()

for photo in [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]:
    photo_folder = os.path.join(base_path, photo)
    num_iterations = len([fol for fol in os.listdir(photo_folder) if os.path.isdir(os.path.join(photo_folder,fol)) and "source" not in fol])
    start_iter = 1
    range_iter = [str(i) for i in list(range(1,num_iterations))]
    folder_base = os.path.join(base_path,photo,photo)

    jsf = []
    for iteration in range_iter:
        jsf += [os.path.join(base_path,photo,photo+"_"+str(iteration),i) for i in os.listdir(os.path.join(base_path, photo, photo+"_"+str(iteration))) if ".json" in i]

    t_ = []
    for j in tqdm(jsf):
        with open(j,'r') as jo:
            tmp = json.load(jo)
        if "pagesWithMatchingImages" not in tmp['responses'][0]['webDetection'].keys():
            continue
        matches = tmp['responses'][0]['webDetection']['pagesWithMatchingImages']
        matches = [i['pageTitle'] for i in matches if "pageTitle" in i.keys()]
        titles = [re.sub('<[^<]+?>', '', i) for i in matches]
        titles = [i.replace("&#39;","'").lower() for i in titles]
        titles = [[i,langid.classify(i)[0]] for i in titles]
        titles = [i for i in titles if i[1] == "en"]
        t_ += titles
    titlesm.update({photo:t_})

def clean_and_split_str(txt):
    #strip_special_chars = re.compile("[^A-Za-z0-9#]+")
    translator = str.maketrans('', '', string.punctuation)
    txt = txt.translate(translator)
    txt = re.sub('\s+', ' ', txt).strip()
    txt = txt.lower()
    return txt

sentences = []

for photo,titles in titlesm.items():
    titles = [clean_and_split_str(t[0]) for t in titles]
    sentences += titles

with open('sentences-titles-en.txt','w') as f:
    for s in sentences:
        f.write(s + " \n")
