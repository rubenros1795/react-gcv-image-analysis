import os,sys
from gcv_api import main
from getImagesFunctions import *
import multiprocessing
from multiprocessing.dummy import Pool as ThreadPool
import concurrent.futures


base_path = os.getcwd()

## Script for assembling images
# Because Google puts a limit on the number of returned 'web results' (url's returned) I do a couple of iterations.

## Step 1: request ~100 web results from source image ('migrant mother') in "mm_source" folder
## Step 2: scrape all images from urls found in the first iteration input_folder

source_image_folder = "C://Users//Ruben//Documents//GitHub//ReACT_GCV//code//work//environment2//ks_source"
api_key = "AIzaSyBgfZktfle4jXZ8AkhsTbdaIWO1pyQx-5s"
image_folder_base = "image_ks_"
processed_urls = []

for n in range(1,7):
    print('--- Iteration ' + str(n))
    if n == 1:
        main.main(input_folder = source_image_folder,
                key = api_key,
                output_folder = image_folder_base,
                iteration = n)

    elif n > 1:

        # Construct List of URLs from .json files
        current_image_folder = image_folder_base + str(n-1)
        list_json = [f for f in os.listdir(current_image_folder) if '.json' in f]
        all_url = []
        for js in list_json:
            json_data = loadJson(os.path.join(current_image_folder,js))

            try:
                temp_url = getImageURL(json_data)
                all_url = all_url + temp_url
            except KeyError:
                print('corrupted json file, probably an 400 Error!')
                continue
        all_url = list(set(all_url))
        all_url = [u for u in all_url if u not in processed_urls]

        # Create destination folder for images
        images_destination = os.path.join(base_path,current_image_folder,'img')
        if not os.path.exists(images_destination):
            os.makedirs(images_destination)

        # Scrape Images
        print(' --Scraping {} images to {}'.format(len(all_url), images_destination))
        #scraperOne(all_url, images_destination)
        os.chdir(os.path.join(base_path,current_image_folder,'img'))
        with concurrent.futures.ThreadPoolExecutor() as e:
            for u in tqdm(all_url):
                e.submit(scraperTwo, u)
        os.chdir(os.path.join(base_path))

        processed_urls = processed_urls + all_url

        # Request API web detection with scraped images as output
        main.main(input_folder = os.path.join(base_path,current_image_folder, 'img'),
                key = api_key,
                output_folder = image_folder_base,
                iteration = n)

with open('processed_urls.txt', 'w') as f:
    for pu in processed_urls:
        f.write(pu + ' /n')
