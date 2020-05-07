from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import json
import uuid
import codecs
import os
import concurrent.futures
from functions import *

for topfolder in ["selection"]:

    base_path = "/media/ruben/Data Drive/react-data/protest/{}".format(topfolder)

    for photo in [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]:

        print('INFO: working on {}'.format(photo))
        photo_folder = os.path.join(base_path, photo)
        num_iterations = len([fol for fol in os.listdir(photo_folder) if os.path.isdir(os.path.join(photo_folder,fol)) and "source" not in fol])
        start_iter = 1
        range_iter = [str(i) for i in list(range(1,num_iterations+1))]
        folder_base = os.path.join(base_path,photo,photo)

        list_fn = dict()

        for it in range_iter:
            fp = os.path.join(base_path,photo,photo+"_"+str(it),"html")
            fps = [os.path.join(fp,i) for i in os.listdir(fp) if ".html" in i]
            list_fn.update({it:fps})

        d_ = dict()

        for it,list_ in list_fn.items():
            d_.update({it:dict()})
            list_context = []

            for u in list_:
                context_images = IM.imgTag(u)
                if context_images is not None:
                    d_[it].update({u:context_images})

        cn = {}
        for iteration, dict1 in d_.items():
            cn.update({iteration:dict()})
            for fn,imgs in dict1.items():

                commas = [item for sublist in [i.split(',') for i in imgs if "," in i] for item in sublist]
                imgs = list(set(imgs + commas))

                correct = [i for i in imgs if "?w" not in i]
                potentials = [i.split("?w") for i in imgs if "?w" in i]

                for pbase in list(set([i[0] for i in potentials])):
                    all_p = [i for i in potentials if i[0] == pbase]
                    pdef = "?w".join(all_p[0])
                    if "," in pdef:
                        [correct.append(i) for i in pdef.split(',')]
                    else:
                        correct.append(pdef)
                cn[iteration].update({fn:correct})

        print('INFO: Dictionary made: {}'.format(os.path.join(base_path,photo,'context-images.json')))
        with open(os.path.join(base_path,photo,'context-images.json'), 'w') as fp:
            json.dump(cn, fp)

        urls = cn

        context_images_path = os.path.join(base_path,photo,"context_images")

        if not os.path.exists(context_images_path):
            os.makedirs(context_images_path)

        # Enable threading for faster scraping (requires function that works with single url)
        os.chdir(context_images_path)

        for k,v in urls.items():

            for page,all_url in v.items():
                with concurrent.futures.ThreadPoolExecutor() as e:
                    for u in all_url:
                        e.submit(IM.scraperTwo, u)

        list_images = [l for l in os.listdir(context_images_path) if ".png" in l or ".jpg" in l or ".Jpeg" in l or ".Jpg" in l]
        small_images = [l for l in list_images if int(os.stat(l).st_size) < 1500]

        for i in small_images:
            os.remove(os.path.join(context_images_path,i))

        list_images = [l[:-4] for l in os.listdir(context_images_path) if ".png" in l or ".jpg" in l]
        list_redtxt = [l for l in os.listdir(context_images_path) if ".txt" in l and l[:-4] not in list_images]
        for i in list_redtxt:
            os.remove(os.path.join(context_images_path,i))
