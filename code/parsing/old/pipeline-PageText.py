from functions import *
from random import sample
from htmldate import find_date
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import json


'''
Step 1: Scrape Pages
'''

for topfolder in ["npg"]:

    base_path = "/media/ruben/Data Drive/react-data/{}".format(topfolder)

    for photo in [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]:
        print('INFO: working on {}'.format(photo))
        photo_folder = os.path.join(base_path, photo)
        num_iterations = len([fol for fol in os.listdir(photo_folder) if os.path.isdir(os.path.join(photo_folder,fol)) and "source" not in fol])
        start_iter = 1
        range_iter = [str(i) for i in list(range(1,num_iterations+1))]
        folder_base = os.path.join(base_path,photo,photo)

        for iteration in range_iter:

            jsFiles = Organize.gatherJson(folder_base,iteration)

            '''
            Step 1a: Find previously scraped urls
            '''

            ## Import previously scraped ones:

            scraped_urls = []
            for i in range(1,int(iteration)):
                try:
                    with open(os.path.join(folder_base + "_" + str(i), "html","results.txt"), 'r', encoding='utf-8') as f:
                        print("INFO: importing from {}".format(os.path.join(folder_base + "_" + str(i), "html","results.txt")))
                        lu = f.readlines()
                        lu = [l.split('|') for l in lu]
                        lu = [l for l in lu if len(l) == 2]
                        lu = [l[1].replace('\n','') for l in lu]
                        scraped_urls = scraped_urls + lu
                except FileNotFoundError:
                    print("INFO: ", os.path.join(folder_base + "_" + str(i), "html","results.txt"), "not found")

            print('INFO: found {} urls in iterations {}-{}'.format(len(scraped_urls),1,int(iteration)-1))

            '''
            Step 1b: Scrape All Page URLs to 'image[...]/html' folder
            '''
            destination_path = os.path.join(folder_base + "_" + str(iteration), "html")
            HTML.Log(destination_path, "results.txt")

            list_urls = list(set([j['url'] for j in jsFiles]))
            print('INFO: {} urls found in .json files for iteration {}'.format(len(list_urls),iteration))

            list_urls = [u for u in list_urls if u not in scraped_urls]
            print('INFO: {} urls left after duplicate detection'.format(len(list_urls)))

            HTML.PoolScrape(list_urls, destination_path)
            print('INFO: scraping htmls iteration {} finished'.format(iteration))

        '''
        Step 3: Scrape Text
        '''
        print("INFO: scraping tet for {}".format(photo))
        for iteration in range_iter:
            ParseText.Parse(os.path.join(folder_base+ "_" + str(iteration), "html"))
