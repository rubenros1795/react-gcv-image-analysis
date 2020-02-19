import os,sys
from gcv_api import main
from getImagesFunctions import *
from getDataFunctions import *
import multiprocessing
from multiprocessing.dummy import Pool as ThreadPool
import concurrent.futures

base_path = os.getcwd()
image_folder_base = "image_npg_"
n = 4

processed_urls = []

for i in range(1,n+1):
    print("looking in {}".format()
    list_ = gatherProcessedImagessUrls(os.path.join(base_path,image_folder_base+str(i),"img"))
    if list_ is not None:
        print("{} scraped images found in {}".format(len(list_)),os.path.join(base_path,image_folder_base+str(i),"img")))
        processed_urls = processed_urls + list_
        processed_urls = list(set(processed_urls))
