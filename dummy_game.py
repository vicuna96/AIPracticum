from game import *
from similarity_algs import *

if __name__ == '__main__':
    source = random_id_generator(id_attrib_dict)
    target = random_id_generator(id_attrib_dict)

    metric = get_doc2vec_gensim()
#    metric = get_spacy_metric()
    priority_beam_search(source, target, 5, metric)