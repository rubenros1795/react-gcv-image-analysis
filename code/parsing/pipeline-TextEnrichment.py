from functions import *
from random import sample
from htmldate import find_date
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import json
from langid.langid import LanguageIdentifier, model
import spacy

base_path = "/media/ruben/Data Drive/react-data/npg"

for photo in [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]:

    print('INFO: working on {}'.format(photo))
    photo_folder = os.path.join(base_path, photo)
    num_iterations = [fol for fol in os.listdir(photo_folder) if os.path.isdir(os.path.join(photo_folder,fol)) and "source" not in fol and "context" not in fol]
    num_iterations = len(num_iterations)

    start_iter = 1
    range_iter = [str(i) for i in list(range(1,num_iterations + 1))]
    folder_base = os.path.join(base_path,photo,photo)

    # Import Texts from all iterations
    df = pd.DataFrame()

    for iteration in range_iter:
        with open(folder_base+"_"+str(iteration)+"/txt/parsed_text.json",'r') as fp:
            text_dict_tmp = json.load(fp)
        texts = [['||'.join(sents),id] for id,sents in text_dict_tmp.items()]
        ids = [t[1] for t in texts]
        texts = [t[0] for t in texts]
        languages = [identifier.classify(i)[0] for i in texts]
        tmp = pd.DataFrame([texts,languages,ids]).T
        df = df.append(tmp)
    df.columns = ['text','lang','id']

    ## NER
    identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)
    selected_languages = "en de fr es it nl pt".split(' ')
    selected_languages = {i:i+"_core_news_sm" for i in selected_languages}
    selected_languages.update({"en":"en_core_web_sm"})
    print('INFO: Entity Recognition on: {}'.format(" ".join([i for i in list(set(df['lang'])) if i in selected_languages.keys()])))

    d_ = dict()
    for lang in list(set([i for i in list(set(df['lang'])) if i in selected_languages.keys()])):
        print('INFO: Photo: {} | Language: {}'.format(photo,lang))
        if lang not in d_.keys():
            d_.update({lang:dict()})
        nlp = spacy.load(selected_languages[lang])
        tmp = df[df['lang'] == lang].reset_index(drop=True)
        print('INFO: found {} webpages'.format(len(tmp)))

        for count,text in tqdm(enumerate(tmp['text'])):
            identif = str(tmp['id'][count])
            d_[lang].update({identif:dict()})
            d_[lang][identif].update({"text":text})
            doc = nlp(text)
            doc = [(ent.text, ent.start_char, ent.end_char, ent.label_) for ent in doc.ents]
            d_[lang][identif].update({"entities":doc})

    with open(os.path.join(base_path, photo,"entities-{}.json".format(photo)), 'w') as fp:
        json.dump(d_, fp)

    print('INFO: wrote {}'.format(os.path.join(base_path, photo,"entities-{}.json".format(photo))))
