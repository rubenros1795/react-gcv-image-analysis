from functions import *
from random import sample
from htmldate import find_date
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import json
from langid.langid import LanguageIdentifier, model
import spacy

sampling = True
sample_size = 1000


for topfolder in ["npg"]:

    base_path = "/media/ruben/Data Drive/react-data/{}".format(topfolder)

    for photo in [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]:

        print('INFO: working on {}'.format(photo))
        photo_folder = os.path.join(base_path, photo)
        num_iterations = len([fol for fol in os.listdir(photo_folder) if os.path.isdir(os.path.join(photo_folder,fol)) and "source" not in fol])
        start_iter = 1
        range_iter = [str(i) for i in list(range(1,num_iterations+1))]
        folder_base = os.path.join(base_path,photo,photo)

        print('INFO: Scraping Languages for photo {}'.format(photo))
        language_dict = dict()
        for iteration in tqdm(range_iter):

            language_dict.update({str(iteration):dict()})

            list_json= [js for js in os.listdir(os.path.join(base_path,photo,photo + "_" + str(iteration),"txt")) if ".json" in js]

            df = pd.DataFrame()
            if len(list_json) > 0:
                for js in list_json:
                    with open(os.path.join(base_path,photo,photo + "_" + str(iteration),"txt", js)) as f:
                        d_ = json.load(f)
                    val = [" ".join(i) for i in d_.values()]
                    ids = [i for i in d_.keys()]
                    val = pd.DataFrame([ids,val]).T
                    val.columns = ['id','text']
                    df = df.append(val)
            else:
                print('no .json files found')

            df['url'] = [i.split('.html_')[1] for i in df['id']]


            for c,url in enumerate(df['url']):

                language_score = Language.ParseUrl(url)

                if language_score is None or language_score[1] < 0.7:
                    try:
                        language_score = Language.ParseText(str(df['text'][c])[1:-1])
                        language_score.append('text')
                    except Exception as e:
                        continue
                else:
                    language_score.append('url')

                language_dict[str(iteration)].update({url:[language_score[0],language_score[1],language_score[2]]})


        # B. Write Detected Languages to language.json
        print("INFO: Writing detected languages to {}".format(os.path.join(photo,'languages.json')))
        with open(os.path.join(base_path,photo,'languages-{}.json'.format(photo)), 'w') as fp:
            json.dump(language_dict, fp)

        '''
        Step 2: Scrape Date
        '''
        scraped_urls = dict()
        print('INFO: Gathering URLs for Date Detection')

        for iteration in range_iter:
            try:
                with open(os.path.join(base_path, photo, photo + "_" + str(iteration), "html", "results.txt"), 'r', encoding='utf-8') as f:
                    lu = f.readlines()
                lu = [l.split('|') for l in lu]
                lu = [l for l in lu if len(l) == 2]
                lu = [l[1].replace('\n','') for l in lu]
                print("---- {} dates found in iteration {}".format(len(lu),iteration))
                scraped_urls.update({str(iteration):lu})
            except Exception as e:
                print("Error: ",e)

        print('INFO: Scraping Dates')

        # lOGGING IN A SEPARATE FILE: NEEDS FIXING
        #HTML.Log(os.path.join(base_path,photo),filename='dates-{}.txt'.format(photo))

        # for k,v in scraped_urls.items():
        #
        #     print('---- Scraping Dates Iteration {}, {} URLs'.format(k,len(v)))
        #     if sampling == True:
        #         print('----- Sampling with Size {}'.format(sample_size))
        #         if len(v) < sample_size:
        #             v = v
        #         else:
        #             v = random.sample(v,sample_size)
        #
        #     WebPage.PoolScrapeDate(v, os.path.join(base_path,photo),os.path.join(base_path,photo,"dates.txt"))

        # SCRAPE DATES ONE BY ONE: WORKS SLOWER
        dates_dict = dict()
        for it,list_ in scraped_urls.items():
            dates_dict.update({str(it):dict()})
            print('---- Scraping Dates Iteration {}, {} URLs'.format(it,len(list_)))
            if sampling == True:
                print('----- Sampling with Size {}'.format(sample_size))
                if len(list_) < sample_size:
                    list_ =list_
                else:
                    list_ = random.sample(list_,sample_size)

            for u in tqdm(list_):
                try:
                    date = WebPage.gatherSingleDate(u)
                    dates_dict[str(it)].update({u:date})
                except Exception as e:
                    continue

        # E. Write Detected Dates to language.json
        print("INFO: Writing detected dates to {}".format(os.path.join(photo,'dates.json')))
        with open(os.path.join(base_path,photo,'dates-{}.json'.format(photo)), 'w') as fp:
            json.dump(dates_dict, fp)

        #os.remove(os.path.join(base_path,photo,"dates-{}.txt".format(photo)))

        # '''
        # Step 3: Get Entities
        # '''
        # # F. Named Entitiy Recognition using Spacy
        print("INFO: Language Detection & Named Entitiy Recognition using Spacy")

        identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)
        selected_languages = "en de fr es it nl pt".split(' ')
        selected_languages = {i:i+"_core_news_sm" for i in selected_languages}
        selected_languages.update({"en":"en_core_web_sm"})

        def PreProc(text):
            text = text[1:-1].replace('\xa0', ' ')
            text = " ".join(text.split('\r\n'))
            return text

        d_ = dict()
        for iteration in range_iter:

            # Language Detection
            list_csv = [csv for csv in os.listdir(os.path.join(base_path, photo, photo + "_" + str(iteration),"txt")) if ".csv" in csv]

            df= pd.DataFrame()
            for csv in list_csv:
                tmp = pd.read_csv(os.path.join(base_path, photo, photo + "_" + str(iteration),"txt",csv))
                df = df.append(tmp)

            df['text'] = [PreProc(str(i)) for i in df['text']]
            df['lang'] = [identifier.classify(i)[0] for i in df['text']]
            df.to_csv(os.path.join(base_path, photo, "text-language-{}.csv".format(photo)),index=False)

            # NER
            for lang in [i for i in list(set(df['lang'])) if i in selected_languages.keys()]:
                if lang not in d_.keys():
                    d_.update({lang:dict()})
                nlp = spacy.load(selected_languages[lang])
                tmp = df[df['lang'] == lang]

                for count,text in enumerate(df['text']):
                    identif = str(df['id'][count])
                    d_[lang].update({identif:dict()})
                    d_[lang][identif].update({"text":text})
                    doc = nlp(text)
                    doc = [(ent.text, ent.start_char, ent.end_char, ent.label_) for ent in doc.ents]
                    d_[lang][identif].update({"entities":doc})

        with open(os.path.join(base_path, photo,"entities-{}.csv".format(photo)), 'w') as fp:
            json.dump(language_dict, fp)
