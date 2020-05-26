from functionsLexicalAnalysis import *


data = pd.read_csv(open('/media/ruben/FEF44259F44213F5/Users/Ruben/Documents/GitHub/ReACT_GCV/data/images_tables_article_carlo/data-full-dd-full.csv'),engine='c')
data['sentences'] = [" ".join(str(x).split('||')).replace('||',' ') for x in list(data['sentences'])]

################# Vocabularies ##################
violence_vocab_nouns = ['violenza','violenze']
violence_vocab_adjs = ['violente','violenta','violento']
protesters_vocab = ['manifestanti','manifestante','dimostranti','dimostrante','contestatori','contestatore','attivisti','attiviste','facinorosi','facinorosi','militanti']
protests_vocab = "dimostrazione manifestazione manifestazioni dimostrazioni".split(' ')
police_vocab = ["forze dell'ordine",'carabinieri','carabineri','carabinierii','carabineiri','polstrada','polizia','poliziotti','carabiniere','agente','agenti']
police_vocab_extensions = ["forze di polizia", "forze dell'ordine", "forze  dell'ordine", "forze  dell’ordine", "forze dell’ordine"]
photo_vocab = "foto fotografie immagini immagine".split()

###

extension_dict = {" CARLO ": [" carlo giuliani ", " carlo ", " giuliani "],
                  "polizia": ["forze di polizia", "forze dell'ordine", "forze  dell'ordine", "forze  dell’ordine", "forze dell’ordine"]}

# NounVerbPairs('it',photo_vocab,verbose=True,export=True,fn = "photo-nouns-verbs-replaced-it.csv",extension_dict=extension_dict)
# Transform2Counts('/media/ruben/FEF44259F44213F5/Users/Ruben/Documents/GitHub/ReACT_GCV/data/images_tables_article_carlo/photo-nouns-verbs-replaced-it.csv',type_a='NVP')

for vocab in [protests_vocab,protesters_vocab,['polizia'],['CARLO'],violence_vocab_nouns]:
    # PMI(keywords = vocab,
    #     extension_dict = extension_dict,
    #     language = "italian",
    #     language_code = "it",
    #     threshold = 25
    #     )

    NounAdjPairs('it',
                vocab,
                verbose=True,
                export=True,
                fn="-".join(vocab) + "-noun-adjective-pair.csv",
                extension_dict=extension_dict)

    NounAdjPairs('it',
                vocab,
                verbose=True,
                export=True,
                fn="-".join(vocab) + "-noun-verb-pair.csv",
                extension_dict=extension_dict)
