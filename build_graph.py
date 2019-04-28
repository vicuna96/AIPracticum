import string
import nltk
import numpy as np
import xml.etree.ElementTree as ET
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def tokenize(text):
    text = text.lower().translate(str.maketrans('', '', string.punctuation))
    stemmer = PorterStemmer()
    tokens = nltk.word_tokenize(text)
    stems = stem_tokens(tokens, stemmer)
    return stems

def calc_tfs(corpus):
    tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
    tfs = tfidf.fit_transform(corpus)
    return tfidf, tfs

# def cos_sim(a, B):
#     print(a.shape, B.shape)
#     return np.dot(a, B) / (np.linalg.norm(a) * np.linalg.norm(b))

def get_cos_sim(query_str, corpus):
    tfidf, tfs = calc_tfs(corpus)
    response = tfidf.transform([query_str])
    return cosine_similarity(response, tfs)

def find_page_by_id(root, id_n):
    page = root.find(".//links/..[@id='" + id_n + "']")
    links = page.find('links').text.split()
    # title = page.find('title').text
    text = page.find('text').text
    print('found page ', id_n)
    return (links, text)

def get_children(root, links):
    return [find_page_by_id(root, id_n)[1] for id_n in links]

def links_by_cosim(root, id_n):
    links, text = find_page_by_id(root, id_n)
    children = get_children(root, links)
    cosims = get_cos_sim(text, children)
    inds = np.argsort(cosims)
    sorted_links = np.asarray(links)[inds].tolist()[0]
    return sorted_links

if __name__ == '__main__':
    tree = ET.parse('wikipedia-051105-preprocessed/20051105_pages_articles.hgw.xml')
    root = tree.getroot()
    links_by_cosim(root, '309')


corpus = ['This is the first document.','This document is the second document.','And this is the third one.','Is this the first document?']
