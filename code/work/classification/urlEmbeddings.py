from gensim.models import FastText
import os,sys
from gcv_api import main
sys.path.insert(1, 'C:/Users/Ruben/Documents/GitHub/ReACT_GCV/code/work/scrape_environment')

from getImagesFunctions import *
from getDataFunctions import *


#model_ted = FastText(sentences_ted, size=100, window=5, min_count=5, workers=4,sg=1)

list_urls = []

for i in range(1,n+1):
    list_ = gatherProcessedImagessUrls(os.path.join(base_path,image_folder_base+str(i),"img"))
            if list_ is not None:
                print("{} scraped images found in {}".format(len(list_),os.path.join(base_path,image_folder_base+str(i),"img")))
                processed_urls = processed_urls + list_
                processed_urls = list(set(processed_urls))
