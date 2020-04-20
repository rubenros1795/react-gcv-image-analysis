from functions import *
from random import sample
from htmldate import find_date
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import json


'''
Step 1: Scrape Pages
'''

for topfolder in ["selection"]:

    base_path = "/media/ruben/Data Drive/react-data/protest/{}".format(topfolder)

    for photo in [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]:
        print('INFO: working on {}'.format(photo))
        photo_folder = os.path.join(base_path, photo)
        num_iterations = len([fol for fol in os.listdir(photo_folder) if os.path.isdir(os.path.join(photo_folder,fol)) and "source" not in fol])
        start_iter = 1
        range_iter = [str(i) for i in list(range(1,num_iterations))]
        folder_base = os.path.join(base_path,photo,photo)

        for iteration in range_iter:

            print("INFO: scraping text for {}".format(photo))
            for iteration in range_iter:
                ParseText.Parse(os.path.join(folder_base+ "_" + str(iteration), "html"))
