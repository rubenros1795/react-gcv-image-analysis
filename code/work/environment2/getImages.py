import os,sys
from gcv_api import main
from scrapeImages import *
import multiprocessing

base_path = os.getcwd()

## Script for assembling images
# Because Google puts a limit on the number of returned 'web results' (url's returned) I do a couple of iterations.

## Step 1: request ~100 web results from source image ('migrant mother') in "mm_source" folder
## Step 2: scrape all images from urls found in the first iteration input_folder

source_image_folder = "C://Users//Ruben//Documents//GitHub//ReACT_GCV//code//work//environment2//ks_source"
api_key = "AIzaSyBgfZktfle4jXZ8AkhsTbdaIWO1pyQx-5s"
image_folder_base = "image_ks_"
processed_urls = []

for n in range(3,5):
    print('iteration ' + str(n))
    if n == 1:
        main.main(input_folder = source_image_folder,
                key = api_key,
                output_folder = image_folder_base,
                iteration = n)
    elif n > 1:
        #print(os.getcwd())
        current_image_folder = image_folder_base + str(n-1)
        #print(current_image_folder)
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

        print('{} image-urls found'.format(len(all_url)))

        images_destination = os.path.join(base_path,current_image_folder,'img')
        #print(images_destination)
        if not os.path.exists(images_destination):
            os.makedirs(images_destination)

        ## TEST
        all_url = all_url[0:50]


        print('scraping')
        pool = multiprocessing.Pool(16)
        for i, url in enumerate(all_url):
            savepath = os.path.join(images_destination, str(i))
            #print(savepath)
            r = pool.apply_async(scrapeImage, (url, savepath))
            print(r)


        print('all images of iteration {} scraped'.format(n))
        exit()
        processed_urls = processed_urls + all_url

        main.main(input_folder = os.path.join(base_path,current_image_folder, 'img'),
                key = api_key,
                output_folder = image_folder_base,
                iteration = n)

with open('processed_urls.txt') as f:
    for pu in processed_urls:
        f.write(pu + ' /n')
