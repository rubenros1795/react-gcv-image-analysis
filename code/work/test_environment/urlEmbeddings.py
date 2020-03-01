from gensim.models import FastText
import os,sys
from urllib.parse import urlparse
from getImagesFunctions import *
from getDataFunctions import *
from gensim.models import Word2Vec
import gensim


#model_ted = FastText(sentences_ted, size=100, window=5, min_count=5, workers=4,sg=1)

urls = gatherPagesUrlsFolder("C:/Users/Ruben/Documents/GitHub/ReACT_GCV/code/work/scrape_environment/image_npg_2")

#sentences_parsed = [[str(i) for i in urlparse(x) if i] for x in urls]
#print(sentences_parsed[0:2])
sentences = [i for i in urls]

#model_parsed = FastText(sentences_parsed, size=100, window=5, min_count=5, workers=4,sg=1)
#model_parsed.save("model_parsed.w2v")

model = FastText(sentences, size=100, window=25, min_count=1, workers=6,sg=1)
model.save("model.w2v")

mp = gensim.models.KeyedVectors.load('model.w2v')
for i in mp.most_similar('www.theguardian.com'):
    print(i)
#print(str(list(mp.wv.vocab)[0:10]))
