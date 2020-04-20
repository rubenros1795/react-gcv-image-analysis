import json,os
from getDataFunctionsClasses import *
import os,sys
from gcv_api import main
from getImagesFunctions import *
from getDataFunctions import *
import multiprocessing
from multiprocessing.dummy import Pool as ThreadPool
import concurrent.futures
from tqdm import tqdm
import argparse



photo = "deniz"
base_path = "/media/ruben/Data Drive/react-data/protest"
image_folder_base = os.path.join(base_path,photo,photo+"_")
n=2

folder_jsons = image_folder_base + str(int(n))
list_json = [f for f in os.listdir(folder_jsons) if '.json' in f]
print(" jsons found: ", len(list_json))

all_url = []
for js in list_json:
    json_data = loadJson(os.path.join(folder_jsons,js))

    try:
        temp_url = getImageURL(json_data)
        all_url = all_url + temp_url
    except KeyError:
        print('corrupted json file, probably an 400 Error!')
        continue
all_url = list(set(all_url))

processed_urls = []

for iter_previous in range(1,int(n)):

    folder_jsons = image_folder_base + str(int(iter_previous))
    list_json = [f for f in os.listdir(folder_jsons) if '.json' in f]

    for js in list_json:
        json_data = loadJson(os.path.join(folder_jsons,js))

        try:
            temp_url = getImageURL(json_data)
            for u in temp_url:
                processed_urls.append(u)
        except KeyError:
            print('corrupted json file, probably an 400 Error!')
            continue
print("{} image-URLs found in previous iterations".format(len(list(set(processed_urls)))))

num_removed = len([u for u in all_url if u in processed_urls])
all_url = [u for u in all_url if u not in list(set(processed_urls))]

if len(all_url) == 0:
    print('0 new urls, breaking loop')
    exit()

print("---- Gathered {} URLs from .json files of API output Iteration {}. Removed {} duplicates".format(len(all_url),int(n),num_removed))


# Create destination folder for images
images_destination = os.path.join(image_folder_base + str(n), "img")
if not os.path.exists(images_destination):
    os.makedirs(images_destination)

# SCRAPE IMAGES
print('----- Scraping {} images to {}'.format(len(all_url), images_destination))
print('...')

# Enable threading for faster scraping (requires function that works with single url)
os.chdir(images_destination)
with concurrent.futures.ThreadPoolExecutor() as e:
    for u in all_url:
        e.submit(scraperTwo, u)
