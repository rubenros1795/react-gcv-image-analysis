from bs4 import BeautifulSoup
import requests
from newspaper import Article
import image_scraper
from getDataFunctions import *
from getImagesFunctions import *

from urllib.parse import urljoin
import json
import uuid

'''
Function for Extracting Images
'''

# Configuration
extensions = ".jpg .JPG .JPEG .jpeg .Jpeg .png .gif .tiff .raw .gif .bmp .ppm".split(' ')

def imgTag(url, classes=False):
    content = requests.get(url).content
    soup = BeautifulSoup(content,'lxml')
    image_tags = soup.findAll('img')
    #tld = tldextract.extract(url)
    #tld = '{}.{}'.format(tld.domain, tld.suffix)
    tld = url


    if classes == True:
        d = dict()

        for c,tag in enumerate(image_tags):
            tmp = dict(tag.attrs)
            if "src" in tmp.keys():
                if "logo" in str(tmp['src']):
                    continue
                elif any(e in str(tmp['src']) for e in extensions):
                    tmp['src'] = urljoin(url, tmp['src'])
                else:
                    continue
            d.update({tmp['src']:tmp})
            d.update({"original_url":url})

    if classes == False:
        d = dict()
        list_url_page = []
        for c,tag in enumerate(image_tags):
            tmp = dict(tag.attrs)
            if "src" in tmp.keys():
                if "logo" in str(tmp['src']):
                    continue
                elif any(e in str(tmp['src']) for e in extensions):
                    list_url_page.append(urljoin(url, tmp['src']))
                else:
                    continue
        d = {url:[str(uuid.uuid4()),list_url_page]}


    return d

# Generate list_urls
list_urls = gatherPagesUrls(name = "image_ks_", n_folders=3)[:10]

d_ = dict()
for u in list_urls:
    d=imgTag(u,classes=False)
    d_.update(d)

with open('context-images.json', 'w') as fp:
    json.dump(d_, fp)

base_path = os.getcwd()
context_images_path = os.path.join(base_path,"image_ks_context")

if not os.path.exists(context_images_path):
    os.makedirs(context_images_path)

for page,v in d_.items():
    url = page
    id = v[0]
    list_url = v[1]
    print(type(list_url))

    if len(list_url) == 0:
        continue
    os.chdir(context_images_path)
    for img in list_url:
        scraperTwo(img)
    os.chdir(base_path)
