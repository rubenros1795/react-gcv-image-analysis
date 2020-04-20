import json,os
import pandas as pd
from PIL import Image
import numpy as np
import urllib
from yurl import URL


def img2url(imgfn):
    imgfn = os.path.join("/media/ruben/Data Drive/react-data/context-images-npg",imgfn)
    urlfn = "".join(imgfn.split('.')[:-1]) + ".txt"
    with open(urlfn,'r') as txt:
        c = txt.readlines()

    c = c[0]
    c = c.split(":")[-1]
    c = URL(c)[2]
    return c

with open("/media/ruben/Data Drive/react-data/duplicates.json",'r') as fp:
    d = json.load(fp)
    print('loaded json with {} items'.format(len(d)))

# Disambiguate

nd = {}

for k,v in d.items():

    key = k
    value = v
    len_item = len(value)

    other_items_containing_key = {k:v for k,v in d.items() if key in v}
    other_items_larger_list = {k:v for k,v in other_items_containing_key.items() if len(v) > len_item}

    if len(other_items_larger_list) > 0 or len_item == 1:
        continue
    else:
        nd.update({key:value})
print("disambiguated: {} items".format(len(nd)))


url_d = [[k, v] for k,v in nd.items()]

urldd = {}

for c,i in enumerate(url_d):
    try:
        k = "img"+str(c)
        v = [img2url(i[0])] + [img2url(z) for z in i[1]]
        urldd.update({k:v})
    except:
        print('no')

df = pd.DataFrame()
for img,urls in urldd.items():
    img = img
    urls = list(set(urls))

    for u in urls:
        linked_images = [k for k,v in urldd.items() if u in v]

        if len(linked_images) > 0:
            for l in linked_images:
                tmp = pd.DataFrame([img,l]).T
                df = df.append(tmp)

df.columns = ['source','target']
df.to_csv("/media/ruben/Data Drive/react-data/network.csv",index=False)
