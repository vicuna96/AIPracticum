from gensim.corpora.wikicorpus import WikiCorpus
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import multiprocessing
import numpy as np
import time

"""
Influenced by the Gensim tutorial for Doc2Vec - Wikipedia
https://github.com/RaRe-Technologies/gensim/tree/develop/docs/notebooks
"""

class TaggedWikiDocument(object):
    def __init__(self, wiki):
        self.wiki = wiki
        self.wiki.metadata = True
    def __iter__(self):
        counter = 0
        stamp = time.time()
        for content, (page_id, title) in self.wiki.get_texts():
            counter += 1
            if counter % 10000 == 0:
                print(counter, "time", time.time() - stamp)
                stamp = time.time()
            yield TaggedDocument([c for c in content], [title])
        print("Finished counter at", counter)

folder = ""
file = "enwiki-latest-pages-articles-april23.xml.bz2"
model_name = "big_doc2vec.model"

print("Getting WikiCorpus")

wiki = WikiCorpus(folder+file)

documents = TaggedWikiDocument(wiki)

cores = multiprocessing.cpu_count()

# PV-DBOW 
model = Doc2Vec(dm=0, dbow_words=1, vector_size=200, window=8, min_count=19, epochs=5, workers=cores)

print("Building vocab")

model.build_vocab(documents)

print("Training model")

model.train(documents, total_examples=model.corpus_count, epochs=model.epochs)

print("Saving model as "+str(model_name))

model.save(model_name)

print("Model saved")
