from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from build_graph import *

folder = "models/"
word2vec = "GoogleNews-vectors-negative300.bin.gz"

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
    return cosine_similarity(response1, response2)[0,0]


def get_word2vec(id_attrib_dict, id2):
    import gensim
    model = gensim.models.KeyedVectors.load_word2vec_format(folder+word2vec, binary=True)

    title2 = id_attrib_dict[id2]['title']

    words2 = list(filter(lambda x: x in model.vocab, title2.lower().split(" ")))

    def simi(id_attrib_dict, id1, id2, optional=None):
        title1 = id_attrib_dict[id1]['title']
        words1 = list(filter(lambda x: x in model.vocab, title1.lower().split(" ")))
        if len(words1) == 0:
            return 0
        sim = model.wv.n_similarity(words1, words2)
        return .5 * np.mean(sim) + .5 * np.max(sim)

    return simi

"""
Similarity metric #3: using spacy's en_core_web_lg model
"""
def get_spacy_metric():
    import spacy
    nlp = spacy.load("en_core_web_lg")
    def spc_met(id_attrib_dict, id1, id2, optional=None):
        title1 = id_attrib_dict[id1]['title']
        title2 = id_attrib_dict[id2]['title']
        return nlp(title1).similarity(nlp(title2))
    return spc_met

"""

Similarity metric #4: using a doc2vec model we trained on 
Wikipedia using Gensim
"""
def get_doc2vec_gensim(id_attrib_dict, target):
    from gensim.models.doc2vec import Doc2Vec
    model = Doc2Vec.load('models/big_doc2vec.model')
    doc2 = id_attrib_dict[target]
    try:
        vec2 = model[doc2['title']]
    except:
        vec2 = model.infer_vector(doc2['text'])
    vec2 = vec2 / np.sum( vec2 ** 2)
    def doc2vec_met(id_attrib_dict, id1, id2, optional=None):
        doc1 = id_attrib_dict[id1]
        try:
            vec1 = model[doc1['title']]
        except:
#            print("Document 1 not found",doc1['title'])
            vec1 = model.infer_vector(doc1['text'])
        vec1 = vec1 / np.sum( vec1 ** 2)
        return np.dot(vec1, vec2)
    return doc2vec_met

"""
List of ordered links of current id in order of decreasing similarity based on metric
"""
def links_by_sim(id_attrib_dict, id_current, id_target, metric, optional=None):
    links = [id_link for id_link in id_attrib_dict[id_current]['links'] if id_link in id_attrib_dict]
#    print("Unsorted", [id_attrib_dict[id]['title'] for id in links])
    sims = [metric(id_attrib_dict, id_child, id_target, optional=optional) for id_child in links]
    inds = np.argsort(sims)
    sorted_links = np.asarray(links)[inds[::-1]].tolist()
#    print("Sorted", [id_attrib_dict[id]['title'] for id in sorted_links])
    return sorted_links

if __name__ == '__main__':
    pickle_path_list = ['data/id_attrib_dict_' + str(i) for i in range(1,2)]
    id_attrib_dict = load_data(pickle_path_list)
    tfidf, tfs = calc_tfs(id_attrib_dict)
    source = random_id_generator(id_attrib_dict)
    target = random_id_generator(id_attrib_dict)
    links = links_by_sim(id_attrib_dict, source, target, tf_idf_cos_sim)
