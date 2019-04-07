from gensim.corpora.wikicorpus import WikiCorpus
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import multiprocessing
import numpy as np
import os
from datetime import datetime

class TaggedWikiDocument(object):
    def __init__(self, wiki):
        self.wiki = wiki
        self.wiki.metadata = True
    def __iter__(self):
        for content, (page_id, title) in self.wiki.get_texts():
            yield TaggedDocument([c for c in content], [title])

class TaggedWikiDocuments(object):
    def __init__(self, wikis):
        self.wikis = wikis
    def __iter__(self):
        itera = 0
        for iterator in self.wikis:
            for docu in iterator:
                yield docu
            print("Finished",itera)
            itera += 1

cores = multiprocessing.cpu_count()

# PV-DBOW
model = Doc2Vec(dm=0, dbow_words=1, size=200, window=8, min_count=19, epochs=6, workers=cores)

folder = "/wiki/"
model_name = "wiki.big.doc2vec.model"

wiki_list = os.listdir(folder)
print("wiki list: ",wiki_list)

# np.random.seed(4701)
# sampleIndex = np.random.choice(np.arange(len(wiki_list)), size=20, replace=False)

documents = []
for file in np.array(wiki_list):
    time = -datetime.now()
    wiki = WikiCorpus(folder+file)
    print("Time wiki",time+datetime.now())
    documents.append(TaggedWikiDocument(wiki))

docs = TaggedWikiDocuments(documents)
time = -datetime.now()
model.build_vocab(docs)
print("Time to build vocab", time + datetime.now())

time = -datetime.now()
model.train(documents, total_examples=model.corpus_count, epochs=model.epochs)
print("Time to train", time + datetime.now())

model.save(model_name)