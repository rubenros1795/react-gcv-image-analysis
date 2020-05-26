import os,sys
from gcv_api import main
from functions import *
import multiprocessing
from multiprocessing.dummy import Pool as ThreadPool
import concurrent.futures
from tqdm import tqdm
import argparse
from PIL import Image
import numpy as np


## Script for assembling images
# Because Google puts a limit on the number of returned 'web results' (url's returned) I do a couple of iterations.

## Step 1: request ~100 (max. number of) web results from source image in source folder
## Step 2: scrape all images from urls found in the first iteration input_folder
## Step 3: repeat this iteration n times
## Stept 4: write names of unique scraped urls to .txt file

parser = argparse.ArgumentParser()

parser.add_argument('-p', '--photo', dest="photo", required=True)
parser.add_argument('-i', '--iteration', dest="iteration", required=True)
args = parser.parse_args()

photo = args.photo
n = args.iteration

# Configuration
base_path = "/media/ruben/Data Drive/react-data/protest/charlie"
api_key = ""
print('Working on Photo: {}, Iteration'.format(photo,n))


# Post Images to API
if int(n) == 1:
    input_folder_ = os.path.join(base_path, photo, photo + "_" + "source")

if int(n) > 1:
    input_folder_ = os.path.join(base_path, photo, photo + "_" + str(int(n)-1), "img")

try:
    main.main(
            input_folder = input_folder_,
            key = api_key,
            output_folder = os.path.join(base_path, photo, photo + "_"),
            iteration = n
            )
except Exception as e:
    print(e)
    dfr = dfr.append(pd.DataFrame([photo,int(n)-1]).T)
    exit()

# Gather Image URLs from Output files (.json files) and (if n > 1) remove duplicates
list_json = [os.path.join(base_path, photo, photo + "_" + str(n),f) for f in os.listdir(os.path.join(base_path,photo,photo + "_" + str(n))) if '.json' in f]
print('looking for scraped URLs in {}'.format(list_json))
image_url_current = Json.extract_image_folder(list_json)

if int(n) > 1:
    processed_urls = []
    for iter_previous in range(1,int(n)):
        list_json_prev = [os.path.join(base_path, photo, photo + "_" +str(iter_previous),f) for f in os.listdir(os.path.join(base_path,photo,photo + "_" + str(iter_previous))) if '.json' in f]
        print('looking for previous URLs in {}'.format(list_json_prev))
        image_url = Json.extract_image_folder(list_json_prev)
        processed_urls = processed_urls + image_url

    duplicates = [u for u in image_url_current if u in processed_urls]
    print("{}/{} image-URLs removed (duplicates)".format(len(duplicates),len(image_url_current)))
    image_url_current = [u for u in image_url_current if u not in list(set(processed_urls))]

# Check if there are Images to Scrape, if not: break and go to next Photo
if len(image_url_current) == 0 or image_url_current is None:
    print("No URLs found in Iteration {}, going to next photo".format(n))
    exit()

# Scrape images
images_destination = os.path.join(base_path,photo,photo + "_" + str(n), "img")
if not os.path.exists(images_destination):
    os.makedirs(images_destination)

os.chdir(images_destination)
Im.Scrape(image_url_current)

# Remove duplicates
if len(image_url_current) > 1:
    Im.RemoveSmall(images_destination,4000)
    Duplicates.remove(images_destination)
