from bs4 import BeautifulSoup
import requests
#import tldextract

'''
Function for Extracting <img> tags from html. Gets the tags through bs4 parser and find "src" attribute. 
Some sources are "internal": not linked to a protocol name: ("http://")
The tldextract packages recognizes top level domain: ("google.com") 
It uses the TLD to construct a complete link to image.
'''
url = ""

def imgTag(url):
    content = requests.get(url).content
    soup = BeautifulSoup(content,'lxml')
    image_tags = soup.findAll('img')
    #tld = tldextract.extract(url)
    #tld = '{}.{}'.format(tld.domain, tld.suffix)
    tld = url
    d = dict()
    
    for c,tag in enumerate(image_tags):
        tmp = dict(tag.attrs)
        if "src" in tmp.keys():
            tmp['src'] = urljoin(url, tmp['src'])
        d.update({'{}_{}'.format(tld,c):tmp}) 
        
    d.update({"original_url":url})
    return d
