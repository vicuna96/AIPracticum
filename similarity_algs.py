from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from build_graph import *

def dummy_fun(doc):
    return doc

def calc_tfs(id_attrib_dict):
    id_to_row = {id_num:index for (id_num, index) in zip(id_attrib_dict.keys(), range(len(id_attrib_dict)))}
    corpus = [id_attrib_dict[id_num]['text'] for id_num in id_attrib_dict]
    tfidf = TfidfVectorizer(
        analyzer='word',
        tokenizer=dummy_fun,
        preprocessor=dummy_fun,
        token_pattern=None)
    tfs = tfidf.fit_transform(corpus)
    return tfidf, tfs, id_to_row

"""
Similarity metric #0: dummy metric for control
"""
def dummy_sim(id_attrib_dict, id1, id2, optional=None):
    return 0

"""
Similarity metric #1: maximum pairwise word embedding cosine similarity
"""
def max_pairwise_embedding_sim(id_attrib_dict, id1, id2, optional=None):
    raise NotImplementedError

"""
Similarity metric #2: tf-idf cosine similarity
"""
def tf_idf_cos_sim(id_attrib_dict, id1, id2, optional=None):
    tfs = optional['tfs']
    id_to_row = optional['id_to_row']
    response1 = tfs[id_to_row[id1]]
    response2 = tfs[id_to_row[id2]]
    return float(cosine_similarity(response1, response2))

"""
Similarity metric #3: using spacy's en_core_web_lg model
"""
def get_spacy_metric():
    import spacy
    nlp = spacy.load("en_core_web_lg")
    def spc_met(id_attrib_dict, id1, id2, optional=None):
        title1 = id_attrib_dict[id1]['title']
        title2 = id_attrib_dict[id2]['title']
        return nlp(title1).similarity(nlp(title1))
    return spc_met

"""

Similarity metric #4: using a doc2vec model we trained on 
Wikipedia using Gensim
"""
def get_doc2vec_gensim():
    from gensim.models.doc2vec import Doc2Vec
    model = Doc2Vec.load('big_doc2vec.model')
    cosine = lambda x, y: np.dot(x / np.sum(x ** 2), y / np.sum(y ** 2))
    def doc2vec_met(id_attrib_dict, id1, id2, optional=None):
        title1 = id_attrib_dict[id1]['title']
        try:
            vec1 = model[title1]
        except:
            vec1 = model.infer_vector(title1.split())
        title2 = id_attrib_dict[id2]['title']
        try:
            vec2 = model[title2]
        except:
            vec2 = model.infer_vector(title2.split())
        return lambda x, y : cosine(vec1, vec2)
    return doc2vec_met

"""
List of ordered links of current id in order of decreasing similarity based on metric
"""
def links_by_sim(id_attrib_dict, id_current, id_target, metric, optional=None):
    links = [id_link for id_link in id_attrib_dict[id_current]['links'] if id_link in id_attrib_dict]
    sims = [metric(id_attrib_dict, id_child, id_target, optional=optional) for id_child in links]
    inds = np.argsort(sims)
    sorted_links = np.asarray(links)[inds].tolist()
    return sorted_links

if __name__ == '__main__':
    pickle_path_list = ['data/id_attrib_dict_' + str(i) for i in range(1,2)]
    id_attrib_dict = load_data(pickle_path_list)
    tfidf, tfs = calc_tfs(id_attrib_dict)
    source = random_id_generator(id_attrib_dict)
    target = random_id_generator(id_attrib_dict)
    links = links_by_sim(id_attrib_dict, source, target, tf_idf_cos_sim)
