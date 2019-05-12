from game import *
from similarity_algs import *

if __name__ == '__main__':
#    source = random_id_generator(id_attrib_dict)
    source = title_to_id['Exponential distribution']
#    target = random_id_generator(id_attrib_dict)
    target = title_to_id['Probability theory']

#    metric = get_doc2vec_gensim()
    metric = get_spacy_metric()
#    metric = tf_idf_cos_sim
    priority_beam_search(source, target, 5, metric, optional={'tfs': tfs, 'id_to_row': id_to_row})
