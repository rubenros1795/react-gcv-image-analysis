#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 16:56:21 2018

@author: jiahuei
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os, time, argparse, numpy as np
import utils, net_params
from tqdm import tqdm

import warnings,json
warnings.filterwarnings("ignore")

pjoin = os.path.join


config = {"network_name":"inception_v3",
          "image_size":0,
          "img_dir":["/media/ruben/Data Drive/react-data/protest/london/london1/context_images/",
                    "/media/ruben/Data Drive/react-data/protest/london/london2/context_images/",
                    "/media/ruben/Data Drive/react-data/protest/london/london3/context_images/"],
          "difference_threshold":95
         }

if __name__ == '__main__':


    net_name = config["network_name"]
    in_size = config["image_size"]
    emb_dtype = np.float16
    img_dir = config["img_dir"]

    recursive_list = True
    cache_resized_img = True
    gpu_id = str(0)
    print('INFO: Using GPU #{}.'.format(gpu_id))

    dist_threshold = config["difference_threshold"]
    if dist_threshold < 1 or dist_threshold > 100:
        print('INFO: Using the default difference threshold of `10`.')
        dist_threshold = 10
    dist_threshold = float(dist_threshold) / 1000

    dirs = img_dir

    # Maybe download checkpoint file
    os.environ['CUDA_VISIBLE_DEVICES'] = gpu_id
    network = net_params.get_net_params(net_name)

    if in_size < network['default_input_size'] or in_size > 1024:
        print('INFO: Using the default input size for `{}`.'.format(network['name']))
        in_size = network['default_input_size']

    cname = '{}_@_{}_@_{}'.format(network['name'], network['end_point'], in_size)
    print('INFO: Using `{}` for duplicate detection.'.format(cname))
    time.sleep(0.1)
    utils.maybe_get_ckpt_file(network)

    # Iterate through directories
    img_paths = utils.list_files(dirs, recursive_list)
    print('INFO: Found {:,d} images.'.format(len(img_paths)))
    time.sleep(0.2)

    # Read and resize the images
    imgs = [utils.read_resize(f, in_size, cache_resized_img) for f in tqdm(img_paths)]

    # Run the CNN to retrieve the embeddings
    embeds = utils.get_embeds(network, imgs)

    # Compare
    dup_fnames = utils.get_duplicates(embeds, img_paths, dist_threshold, emb_dtype)
    output_dir = os.path.dirname(img_dir)
    fn = "duplicates" + img_dir.split('/')[-1] + ".json"
    fn = os.path.join(output_dir,fn)

    print('\nINFO: Dumping results to {}, fn={}.'.format(output_dir,fn))
    with open(fn,'w') as fp:
        json.dump(dup_fnames,fp)
