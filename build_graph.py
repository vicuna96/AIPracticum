import string
import nltk
import math
import numpy as np
import xml.etree.ElementTree as ET
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.porter import PorterStemmer
import pickle
import time
import random

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

# random id generator for start and end
def random_id_generator(id_attrib_dict):
    return random.choice(list(id_attrib_dict))

def get_title_from_id(id_num):
    return id_attrib_dict[id_num]['title']

def preprocess(root):
    id_attrib_dict = {}
    l = len(root.findall('page'))
    count = 0
    start = time.time()
    for page in root.findall('page'):
        count += 1
        current = time.time()
        if count % 1000 == 0:
            print(str(round((current-start)/60, 1)) +' minutes...'+ str(round(count/l * 100, 1)) + '%' + ' done')
            if count % 100000 == 0:
                print('pickling at count ' + str(count) + '...')
                pickle.dump(id_attrib_dict, open('data/id_attrib_dict_' + str(math.ceil(count / 100000)), 'wb'))
                id_attrib_dict = {}
        id_num = int(page.attrib['id'])
        title = page.find('title').text
        try:
            links = [int(link) for link in page.find('links').text.split()]
        except:
            link = []
        try:
            text = tokenize(''.join(page.find('text').itertext()))
        except:
            text = []
        id_attrib_dict[id_num] = {'title':title, 'links':links, 'text':text}
    pickle.dump(id_attrib_dict, open('data/id_attrib_dict_' + str(math.ceil(count / 100000)), 'wb'))

def write_data(path):
    tree = ET.parse(path)
    root = tree.getroot()
    print('starting')
    preprocess(root)

def load_data(path_list):
    results = {}
    for path in path_list:
        print('loading ' + path + '...')
        d = pickle.load(open(path, 'rb'))
        results.update(d)
    return results

if __name__ == '__main__':
    xml_path = 'wikipedia-051105-preprocessed/20051105_pages_articles.hgw.xml'
    pickle_path_list = ['data/id_attrib_dict_' + str(i) for i in range(1,11)]

    # Comment this in if you want to generate the data from scratch
    # write_data(xmlpath)

    # Comment this in if you want to load the data in
    # id_attrib_dict = load_data(pickle_path_list)
