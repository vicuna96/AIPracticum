import urllib.request

rand_article_url = 'https://en.wikipedia.org/wiki/Special:Random'

class ArticleSearch:
    def __init__(self, title: str, parent = None):
        self.title = title
        self.parent = parent
    def get_title(self):
        return self.title
    def get_parent(self):
        return self.parent


def get_links(article):
    links = []
    #print('title', article.title)
    article_url = 'https://en.wikipedia.org/wiki/' + article.title
    article_contents = (urllib.request.urlopen(article_url).read(100000000)).decode('utf-8')
    index = article_contents.find('<a href="/wiki/')
    shortened_article = article_contents[index+15:]
    while index >= 0:
        title = shortened_article[:shortened_article.index('"')]
        links.append(title)
        index = shortened_article.find('<a href="/wiki/')
        shortened_article = shortened_article[index+15:]
    return links


"""
start_article_contents = (urllib.request.urlopen(rand_article_url).read(100000000)).decode('utf-8')
sa_title_index1 = start_article_contents.index('<title>')
sa_title_index2 = start_article_contents.index('- Wikipedia')
start_article_title = start_article_contents[sa_title_index1+7:sa_title_index2]


print(start_article_title)
print(get_links(start_article_contents))

end_article_contents = (urllib.request.urlopen(rand_article_url).read(500)).decode('utf-8')
ea_title_index1 = end_article_contents.index('<title>')
ea_title_index2 = end_article_contents.index('- Wikipedia')
end_article_title = end_article_contents[ea_title_index1+7:ea_title_index2]

print(end_article_title)
"""

def print_lineage(end):
    lineage = []
    while end is not None:
        lineage.append(end.get_title())
        end = end.get_parent()
    lineage.reverse()
    print('lineage:', lineage)

def search(start: ArticleSearch, end: ArticleSearch):
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
        curr_links.sort()
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


bfs_article = ArticleSearch('Breadth-first_search')
algorithm_article = ArticleSearch('Algorithm')
baltimore_article = ArticleSearch('Baltimore')
shakey_article = ArticleSearch('Shakey_the_robot')
aicenter_article = ArticleSearch('Artificial_Intelligence_Center')
vertical_bar_article = ArticleSearch('Vertical_bar')
cornell_article = ArticleSearch('Cornell_University')


search(bfs_article, cornell_article)
