"""
This file is meant to assist in removing irrelevant images in the scraping iterations. Considering the appearance of for example, "double" images (two images pasted together),
reuploading this image to the Google Cloud API yields results that stem from an irrelevant one. These need to be removed manually, in order to prevent the introduction of noise.
The script uses the imagededup library to identify clusters of images. This allows for the batch removal of irrelevant images in the file explorer.



Usage in command line:

First, do:

python clean-assist.py --operation cluster --input_folder D:/test/photo1/photo1_2/img

this clusters the photos and gives them cluster-associated file names. After running this, go to the folder and order the files based on name. Now you can easily remove
batches of irrelevant photos. AFter finishing, run:

python clean-assist.py --operation clean --input_folder D:/test/photo1/photo1_2/img

This removes the cluster-filenames and removes the .txt files without any image attached.

"""

from imagededup.methods import PHash
from collections import Counter
import pandas as pd
import argparse
import shutil
import os

phasher = PHash()

parser = argparse.ArgumentParser()

parser.add_argument('-f', '--input_folder', dest="input_folder", required=True)
parser.add_argument('-o', '--operation', dest="operation", required=True)

args = parser.parse_args()

input_folder = args.input_folder
operation = args.operation

######

def Cluster(input_folder):

    img_files = [i for i in os.listdir(input_folder) if ".txt" not in i]

    img_folder = os.path.join(input_folder,"img")

    if not os.path.exists(img_folder):
        os.makedirs(img_folder)

    for im in img_files:
        old_fn = os.path.join(input_folder,im)
        new_fn = os.path.join(img_folder,im)
        shutil.move(old_fn, new_fn)

    # Generate encodings for all images in an image directory
    encodings = phasher.encode_images(image_dir=img_folder)

    # Find duplicates using the generated encodings
    duplicates = phasher.find_duplicates(encoding_map=encodings)
    df = []
    for k,v in duplicates.items():
        if len(v) > 0:
            for it in v:
                df.append([k,it])
        elif len(v) == 0:
            df.append([k,k])
        else:
            continue
    df = pd.DataFrame(df,columns=['a','b'])

    # Transform Duplicate Pairs to Clusters
    def consolidate(sets):
        # http://rosettacode.org/wiki/Set_consolidation#Python:_Iterative
        setlist = [s for s in sets if s]
        for i, s1 in enumerate(setlist):
            if s1:
                for s2 in setlist[i+1:]:
                    intersection = s1.intersection(s2)
                    if intersection:
                        s2.update(s1)
                        s1.clear()
                        s1 = s2
        return [s for s in setlist if s]

    def group_ids(pairs):
        groups = consolidate(map(set, pairs))
        d = {}
        for i, group in enumerate(sorted(groups)):
            for elem in group:
                d[elem] = i
        return d

    df['c'] = df['a'].replace(group_ids(zip(df.a,df.b)))
    print("INFO: {} clusters found".format(len(set(df['c']))))

    # Renaming Files
    single = 0
    multiple = 0

    newfilenames = []
    for i in set(df['c']):
        tmp = df[df['c'] == i]
        tmp = list(set(list(tmp['a']) + list(tmp['b'])))
        if len(tmp) == 1:
            single += 1
            for fn in tmp:
                newfn = "cluster_single_{}_{}".format(i,fn)
                newfilenames.append(newfn)
                newfn = os.path.join(img_folder,newfn)
                oldfn = os.path.join(img_folder,fn)
                os.rename(oldfn,newfn)
        if len(tmp) > 1:
            multiple += 1
            for fn in tmp:
                newfn = "cluster_{}_{}".format(i,fn)
                newfilenames.append(newfn)
                newfn = os.path.join(img_folder,newfn)
                oldfn = os.path.join(img_folder,fn)
                os.rename(oldfn,newfn)


    image_files = newfilenames

    for im in image_files:
        old_fn = os.path.join(img_folder,im)
        new_fn = os.path.join(input_folder,im)
        shutil.move(old_fn, new_fn)

    os.rmdir(img_folder)
    print('INFO: renamed files.')
    print('---- There are {} clusters that have only one image'.format(single))
    print('---- You can now manually select relevant images in {}'.format(input_folder))

def Clean(input_folder):
    ## Remove Cluster Handles
    files = os.listdir(input_folder)
    files = [os.path.join(input_folder,f) for f in files if ".txt" not in f]
    for filename in files:
        split_path = list(os.path.split(filename))
        newpath = os.path.join(split_path[0], split_path[1].split('_')[-1])
        os.rename(filename,newpath)

    print('INFO: remove cluster handles from file names')
    # Remove text files without associated Images
    ids = [x.split('.')[0] for x in os.listdir(input_folder)]
    removables = [os.path.join(input_folder,k + ".txt") for k,v in dict(Counter(ids)).items() if v == 1]
    for rem in removables:
        try:
            os.remove(rem)
        except Exception as e:
            print(e)
    print('INFO: removed text files without associated images')

####

if __name__ == '__main__':
    if operation == "cluster":
        Cluster(input_folder)

    if operation == "clean":
        Clean(input_folder)
