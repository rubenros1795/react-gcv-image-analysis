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

        iteration_folders = [os.path.join(base_path,topfolder,f) for f in os.listdir(photo_folder) if topfolder + "_" in f]
        
        total_html = 0
        
        for ifo in iteration_folders:
            html_folder = os.path.join(ifo,"html")
            print(html_folder)
            
            if os.path.isdir(html_folder):
                  total_html += len([x for x in os.listdir(html_folder) if ".html" in x])
                  print(total_html)
