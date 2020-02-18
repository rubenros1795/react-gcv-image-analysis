from bs4 import BeautifulSoup
import requests
from newspaper import Article
import image_scraper
from getDataFunctions import *
from urllib.parse import urljoin

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
        d = {url:list_url_page}


    return d

# Generate list_urls
list_urls = gatherPagesUrls(name = "image_ks_", n_folders=3)[0:10]

for u in list_urls:
    d=imgTag(u,classes=False)
    print(d)
    print()
    print('-----------------        ----------------------------')
