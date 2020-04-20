import os,sys
from gcv_api import main
from getImagesFunctions import *
from getDataFunctions import *
import multiprocessing
from multiprocessing.dummy import Pool as ThreadPool
import concurrent.futures
from tqdm import tqdm


base_path = os.getcwd()

## Script for assembling images
# Because Google puts a limit on the number of returned 'web results' (url's returned) I do a couple of iterations.

## Step 1: request ~100 (max. number of) web results from source image in source folder
## Step 2: scrape all images from urls found in the first iteration input_folder
## Step 3: repeat this iteration n times
## Stept 4: write names of unique scraped urls to .txt file

for photo in ["amsterdam1","amsterdam2"]:

    # Configuration
    source_image_folder = "D://react-data//protest//{}//{}_source".format(photo,photo)
    api_key = "AIzaSyBgfZktfle4jXZ8AkhsTbdaIWO1pyQx-5s"
    image_folder_base = "D://react-data//protest//{}//{}_".format(photo,photo)
    num_iterations = 6

    for n in range(1,num_iterations+1):
        print('--- Iteration ' + str(n) + '\n')

        # Iteration 1: Detect Source Folder and post to API
        if n == 1:
            main.main(input_folder = source_image_folder,
                    key = api_key,
                    output_folder = image_folder_base,
                    iteration = n)

        # Iteration n (>1): Detect Image URLs in Iteration n-1 folder; scrape the images and post them to API
        elif n > 1:

            # Construct List of URLs from .json files
            folder_previous = image_folder_base + str(n-1)
            list_json = [f for f in os.listdir(folder_previous) if '.json' in f]
            all_url = []
            for js in list_json:
                json_data = loadJson(os.path.join(folder_previous,js))

                try:
                    temp_url = getImageURL(json_data)
                    all_url = all_url + temp_url
                except KeyError:
                    print('corrupted json file, probably an 400 Error!')
                    continue
            all_url = list(set(all_url))
            print("---- Gathered {} URLs from .json files of Iteration {}".format(len(all_url),n-1))

            # FILTERING
            ## Gather all previously scraped image URLs
            processed_urls = []
            for i in range(1,n+1):
                list_ = gatherProcessedImagessUrls(os.path.join(base_path,image_folder_base+str(i),"img"))
                if list_ is not None:
                    print("----- {} scraped images found in {}".format(len(list_),os.path.join(base_path,image_folder_base+str(i),"img")))
                    processed_urls = processed_urls + list_
                    processed_urls = list(set(processed_urls))

            ## Filter JSON-URLs
            all_url = [u for u in all_url if u not in processed_urls]

            # Create destination folder for images
            images_destination = os.path.join(base_path,folder_previous,'img')
            if not os.path.exists(images_destination):
                os.makedirs(images_destination)

            # SCRAPE IMAGES
            print(' --Scraping {} images to {}'.format(len(all_url), images_destination))
            print('...')

            # Enable threading for faster scraping (requires function that works with single url)
            os.chdir(os.path.join(base_path,folder_previous,'img'))
            with concurrent.futures.ThreadPoolExecutor() as e:
                for u in all_url:
                    e.submit(scraperTwo, u)
            os.chdir(os.path.join(base_path))

            processed_urls = processed_urls + all_url

            # Request API web detection with scraped images as output
            main.main(input_folder = os.path.join(base_path,folder_previous, 'img'),
                    key = api_key,
                    output_folder = image_folder_base,
                    iteration = n)
