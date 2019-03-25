import urllib.request

rand_article_url = 'https://en.wikipedia.org/wiki/Special:Random'

start_article_contents = (urllib.request.urlopen(rand_article_url).read(500)).decode('utf-8')
sa_title_index1 = start_article_contents.index('<title>')
sa_title_index2 = start_article_contents.index('- Wikipedia')
start_article_title = start_article_contents[sa_title_index1+7:sa_title_index2]

print(start_article_title)

end_article_contents = (urllib.request.urlopen(rand_article_url).read(500)).decode('utf-8')
ea_title_index1 = end_article_contents.index('<title>')
ea_title_index2 = end_article_contents.index('- Wikipedia')
end_article_title = end_article_contents[ea_title_index1+7:ea_title_index2]

print(end_article_title)

links = []
ta_contents = (urllib.request.urlopen(rand_article_url).read(10000000)).decode('utf-8')
index = ta_contents.find('<a href="/wiki/')
shortened_article = ta_contents[index+9:]
while index >= 0:
    print("Index:", index)
    title = shortened_article[:shortened_article.index('"')]
    links.append(title)
    print("Title:", title)
    index = shortened_article.find('<a href="')
    shortened_article = shortened_article[index+9:]

print(links)
