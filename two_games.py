from game import *
from similarity_algs import *
#import threading

if __name__ == '__main__':
    #source2 = random_id_generator(id_attrib_dict)
    source1 = title_to_id['Machine learning']
    #target2 = random_id_generator(id_attrib_dict)
    target1 = title_to_id['Battle of the Atlantic']

    game = lambda metric : priority_beam_search(source1, target1, 10, metric, optional={'tfs': tfs, 'id_to_row': id_to_row})

    metric = get_doc2vec_gensim(id_attrib_dict, target1)
#    metric = get_spacy_metric()
    metric = tf_idf_cos_sim
    game(metric)

    metric = tf_idf_cos_sim
    game(metric)
    
