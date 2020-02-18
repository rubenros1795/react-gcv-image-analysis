from bs4 import BeautifulSoup
import requests
import tldextract

url = ""

'''
Function for Extracting <img> tags from html. Gets the tags through bs4 parser and find "src" attribute. 
Some sources are "internal": not linked to a protocol name: ("http://")
The tldextract packages recognizes top level domain: ("google.com") 
It uses the TLD to construct a complete link to image.
'''

def imgTag(url):
    content = requests.get(url).content
    soup = BeautifulSoup(content,'lxml') # choose lxml parser
    image_tags = soup.findAll('img')
    
    tld = tldextract.extract(url)
    tld = '{}.{}'.format(tld.domain, tld.suffix)
        
    d = dict()
    
    for c,tag in enumerate(image_tags):
        d.update({'{}_{}'.format(tld,c):tag.attrs})
    
    return d
