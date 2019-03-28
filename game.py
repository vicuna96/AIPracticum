import urllib.request
from datetime import datetime
from dateutil.relativedelta import relativedelta
from termcolor import colored

rand_article_url = 'https://en.wikipedia.org/wiki/Special:Random'

class ArticleSearch:
    def __init__(self, title: str, parent = None):
        self.title = title
        self.parent = parent
    def get_title(self):
        return self.title
    def get_parent(self):
        return self.parent


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

def get_links(article):
    #print('title', article.title)
    article_url = 'https://en.wikipedia.org/wiki/' + article.title
    article_contents = (urllib.request.urlopen(article_url).read(100000000)).decode('utf-8')
    return get_links_from_contents(article_contents)

def print_lineage(end):
    lineage = []
    while end is not None:
        lineage.append(end.get_title())
        end = end.get_parent()
    lineage.reverse()
    print('lineage:', lineage)

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

def limited_dfs(node, goal, depth):
    if depth == 0:
        if node.get_title() == goal.get_title():
            return node
        else:
            return None
    #print('currently checking children of', node.get_title())
    for l in get_links(node):
        if l == goal.get_title():
            print_lineage(ArticleSearch(l, parent = node))
        found = limited_dfs(ArticleSearch(l, parent = node), goal, depth-1)
        if found is not None:
            return found
    return None

def itdeep_search(start, end):
    d = 0
    while True:
        print('depth is', d)
        found = limited_dfs(start, end, d)
        if found is not None:
            return found
        d += 1

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



play_game()

bfs_article = ArticleSearch('Breadth-first_search')
algorithm_article = ArticleSearch('Algorithm')
baltimore_article = ArticleSearch('Baltimore,_Maryland')
shakey_article = ArticleSearch('Shakey_the_robot')
aicenter_article = ArticleSearch('Artificial_Intelligence_Center')
vertical_bar_article = ArticleSearch('Vertical_bar')
cornell_article = ArticleSearch('Cornell_University')

"""
s = datetime.now()
itdeep_search(bfs_article, baltimore_article)
e = datetime.now()
time_taken(s, e)

start_time = datetime.now()
bfs_search(bfs_article, cornell_article)
end_time = datetime.now()

"""
