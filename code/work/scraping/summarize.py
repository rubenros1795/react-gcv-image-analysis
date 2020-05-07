import os,sys
from gcv_api import main
from functions import *
import multiprocessing
from multiprocessing.dummy import Pool as ThreadPool
import concurrent.futures
from tqdm import tqdm
import logging
import time

df = pd.DataFrame()

for topfolder in ["npg"]:

    base_path = "/media/ruben/Data Drive/react-data/{}".format(topfolder)

    for photo in [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]:
        photo_folder = os.path.join(base_path,photo)
        print(photo_folder)

        num_iterations = list(set([f.split("_")[1] for f in os.listdir(photo_folder) if len(f) == 1]))

        jsonfiles = [[os.path.join(base_path,photo,f,j) for j in os.listdir(os.path.join(base_path,photo,f)) if ".json" in j if "dates" not in j] for f in os.listdir(photo_folder)]
        jsonfiles = [f for f in jsonfiles if f]
        jsonfiles = [item for sublist in jsonfiles for item in sublist]

        pages = []
        for js in jsonfiles:
            js = Json.load(js)
            try:
                tmp_pages = [i['url'] for i in js['responses'][0]['webDetection']['pagesWithMatchingImages']]
                pages = pages + tmp_pages
            except Exception as e:
                continue
        num_pages_photo = len(list(set(pages)))
        tmp = pd.DataFrame([photo, num_pages_photo]).T
        df = df.append(tmp)

df.columns = ["name","num_pages"]
df = df.sort_values("num_pages",ascending=False)
df.to_csv(os.path.join(base_path,"results.csv"),index=False)
print(os.path.join(base_path,"results.csv"))
