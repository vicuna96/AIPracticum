import urllib.request
from datetime import datetime
from dateutil.relativedelta import relativedelta
from termcolor import colored
from random import random
from build_graph import *
from similarity_algs import *

# rand_article_url = 'https://en.wikipedia.org/wiki/Special:Random'
# base_url = 'https://en.wikipedia.org/wiki/'
# prefix_url = '<a href="/wiki/'
# canonical_url = '<link rel="canonical" href="https://en.wikipedia.org/wiki/'

class ArticleSearch:
    def __init__(self, id_number, parent = None, relevance = 0):
        self.id_number = id_number
        self.title = id_attrib_dict[id_number]['title']
        self.parent = parent
        self.relevance = relevance
    def get_title(self):
        return self.title
    def get_parent(self):
        return self.parent

"""
#NOT used for priority beam search
def get_links_from_contents(article_contents):
    links = []
    index = article_contents.find('<a href="/wiki/')
    shortened_article = article_contents[index+15:]
    while index >= 0:
        title = shortened_article[:shortened_article.index('"')]
        links.append(title)
        index = shortened_article.find('<a href="/wiki/')
        shortened_article = shortened_article[index+15:]
    return links

#NOT used for priority beam search
def get_links(article):
    #print('title', article.title)
    article_url = 'https://en.wikipedia.org/wiki/' + article.title
    article_contents = (urllib.request.urlopen(article_url).read(100000000)).decode('utf-8')
    return get_links_from_contents(article_contents)

#Used for priority beam search
def get_relevance(article_title, goal):
    #TODO: urrently unimplemented
    return random()

#Used for priority beam search
def insert_article(l, a, n):
    if len(l) == 0:
        l.append(a)
    for i in range(len(l)):
        if a.relevance > l[i].relevance:
            l.insert(i-1, a)
            break
    if len(l) > n:
        del l[-1]

#Used for priority beam search
def get_top_links_from_contents(article_contents, goal, n):
    links = []
    index = article_contents.find('<a href="/wiki/')
    shortened_article = article_contents[index+15:]
    while index >= 0:
        title = shortened_article[:shortened_article.index('"')]
        rel = get_relevance(title, goal)
        insert_article(links, ArticleSearch(title, relevance = rel), n)
        index = shortened_article.find('<a href="/wiki/')
        shortened_article = shortened_article[index+15:]
    # for l in links:
    #     print(l.title)
    return links

#Used for priority beam search
def get_top_links(article, goal, n):
    article_url = 'https://en.wikipedia.org/wiki/' + article.title
    article_contents = (urllib.request.urlopen(article_url).read(100000000)).decode('utf-8')
    return get_top_links_from_contents(article_contents, goal, n)
"""
def lineage(end):
    lineage = []
    while end is not None:
        lineage.append(end.get_title())
        end = end.get_parent()
    lineage.reverse()
    return lineage
"""
#NOT used for priority beam search
def bfs_search(start, end):
    S = []
    discovered = []
    S.append(start)
    discovered.append(start.get_title())
    while len(S) != 0:
        v = S[0]
        S = S[1:]
        if v.get_title() == end.get_title():
            print_lineage(v)
            return
        curr_links = get_links(v)
        #print('currently checking children of', v.get_title())
        #curr_links.sort()
        #print(curr_links)
        for l in curr_links:
            if l not in discovered:
                discovered.append(l)
                if l == end.get_title():
                    l_article = ArticleSearch(l, parent = v)
                    print_lineage(l_article)
                    return
                l_article = ArticleSearch(l, parent = v)
                S.append(l_article)

#NOT used for priority beam search
def limited_dfs(node, goal, depth):
    if depth == 0:
        if node.title == goal.title:
            return node
        else:
            return None
    #print('currently checking children of', node.get_title())
    for l in get_links(node):
        if l == goal.title:
            print_lineage(ArticleSearch(l, parent = node))
        found = limited_dfs(ArticleSearch(l, parent = node), goal, depth-1)
        if found is not None:
            return found
    return None

#NOT used for priority beam search
def itdeep_search(start, end):
    d = 0
    while True:
        print('depth is', d)
        found = limited_dfs(start, end, d)
        if found is not None:
            return found
        d += 1
"""

#Priority beam search function
def priority_beam_search(start_id, end_id, width, metric, optional=None):
        total_checked = 0
        start = ArticleSearch(start_id)
        end = ArticleSearch(end_id)
        discovered = []
        S = [start]
        discovered.append(start_id)
        while len(S) != 0:
            v = S[0]
            S = S[1:]
            if v.id_number == end_id:
                lin = ' -> '.join(lineage(l_article))
                print(lin)
                print('Total checked:', total_checked)
                return total_checked, lineage(l_article)
            curr_links = links_by_sim(id_attrib_dict, v.id_number, end_id, metric, optional=optional)
            # print('currently checking children of', v.title)
            for i in range(min(width, len(curr_links))):
                l = curr_links[i]
                if l not in discovered:
                    total_checked += 1
                    discovered.append(l)
                    if l == end_id:
                        l_article = ArticleSearch(l, parent = v)
                        lin = ' --> '.join(lineage(l_article))
                        print(lin)
                        print('Total checked:', total_checked)
                        return total_checked, lineage(l_article)
                    l_article = ArticleSearch(l, parent = v)
                    S.append(l_article)


"""
def time_taken(start_time, end_time):
    time_dif = relativedelta(end_time, start_time)
    print('This search took %d minutes, %d.%d seconds' % (time_dif.minutes, time_dif.seconds, time_dif.microseconds))

def prompt_step(current, goal):
    print(colored('\n\n%s Links:' % current.get_title(), 'red'))
    curr_links = get_links(current)
    curr_links.sort()
    for l in curr_links:
        print(l)
    while True:
        next_link = input(colored('Which step would you like to take?\n(Reminder, goal is %s)\n' % goal.get_title(), 'red'))
        if next_link in curr_links:
            break
    if next_link == goal.get_title():
        print(colored('You reached the goal!', 'green'))
        print_lineage(ArticleSearch(next_link, parent = current))
        return

    prompt_step(ArticleSearch(next_link, parent = current), goal)

"""


def play_game():

    start_article_contents = (urllib.request.urlopen(rand_article_url).read(100000000)).decode('utf-8')
    sa_title_index1 = start_article_contents.index('<link rel="canonical" href="https://en.wikipedia.org/wiki/')
    sa_title_index2 = start_article_contents[sa_title_index1:].index('"/>')
    start_article_title = start_article_contents[sa_title_index1+58:sa_title_index1+sa_title_index2]
    start_article = ArticleSearch(start_article_title)
    print('Start Article:', start_article_title)


    end_article_contents = (urllib.request.urlopen(rand_article_url).read(100000000)).decode('utf-8')
    ea_title_index1 = end_article_contents.index('<link rel="canonical" href="https://en.wikipedia.org/wiki/')
    ea_title_index2 = end_article_contents[ea_title_index1:].index('"/>')
    end_article_title = end_article_contents[ea_title_index1+58:ea_title_index1+ea_title_index2]
    end_article = ArticleSearch(end_article_title)
    print('End Article:', end_article_title)

    prompt_step(start_article, end_article)

def init_game(test=True):
    if test:
        pickle_path_list = ['data/id_attrib_dict_test']
    else:
        pickle_path_list = ['data/id_attrib_dict_' + str(i) for i in range(1,11)]
    id_attrib_dict = load_data(pickle_path_list)
    tfidf, tfs, id_to_row = calc_tfs(id_attrib_dict)
    title_to_id = create_title_to_id(id_attrib_dict)

    return id_attrib_dict, tfidf, tfs, id_to_row, title_to_id

id_attrib_dict, tfidf, tfs, id_to_row, title_to_id = init_game(test = False)

# priority_beam_search(source, target, 10, tf_idf_cos_sim, optional={'tfs': tfs, 'id_to_row':id_to_row})
# priority_beam_search(source, target, 10, dummy_sim)

paths = [('Jesus', 'Volkswagen'), ('Toothpaste', 'William Shakespeare'), ('Puppy', 'Racism'), ('Pants', 'Shirt'), ('Elmo', 'Teletubbies'), ('Apple pie', 'Rock (geology)'), ('Here', 'There'), ('Oboe', 'Veto'), ('Satyr', 'Wombat'), ('Locust', 'Bicycle')]

spc_met = get_spacy_metric()

def eval_func(paths):
    total_checked = []
    lineage_list = []
    for source_title, target_title in paths:
        source = title_to_id[source_title]
        target = title_to_id[target_title]
        print(source_title, target_title)
        total_checked_0, lin_0 = priority_beam_search(source, target, float('inf'), dummy_sim)
        total_checked_1, lin_1 = priority_beam_search(source, target, 10, tf_idf_cos_sim, optional={'tfs': tfs, 'id_to_row':id_to_row})
        total_checked_2, lin_2 = priority_beam_search(source, target, float('inf'), spc_met)
        total_checked.append((total_checked_0, total_checked_1, total_checked_2))
        lineage_list.append((lin_0, lin_1, lin_2))
    return total_checked, lineage_list

# total_checked, lineage_list = eval_func(paths)




#play_game()
"""
bfs_article = ArticleSearch('Breadth-first_search')
algorithm_article = ArticleSearch('Algorithm')
baltimore_article = ArticleSearch('Baltimore,_Maryland')
shakey_article = ArticleSearch('Shakey_the_robot')
aicenter_article = ArticleSearch('Artificial_Intelligence_Center')
vertical_bar_article = ArticleSearch('Vertical_bar')
cornell_article = ArticleSearch('Cornell_University')

s = datetime.now()
itdeep_search(bfs_article, baltimore_article)
e = datetime.now()
time_taken(s, e)


s = datetime.now()
priority_beam_search(bfs_article, baltimore_article, 5)
e = datetime.now()
time_taken(s, e)


start_time = datetime.now()
bfs_search(bfs_article, cornell_article)
end_time = datetime.now()

"""