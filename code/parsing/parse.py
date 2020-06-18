from secFunctions import *
from functions import *

from random import sample
from htmldate import find_date
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import json


'''
Step 1: Scrape Pages
'''


base_path = "/path/to/photos/"
photo = "2"

# # Parse Texts
# Parse.Texts(base_path,"2")
#
# # Parse Languages
# Parse.Languages(base_path,"2")
#
# # Parse Dates
# Parse.Dates(base_path,"2")
#
# # Parse Entities
# Parse.Entities(base_path,"2")

# Parse ContextImages
Parse.ContextImages(base_path,"2")
