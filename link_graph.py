from article import Article
import pickle

def build_id_title_dict(titles_file):
    '''
    Returns dictionary where key is article id and value is article title
    titles_file: text file of Wikipedia article names
    '''
    id_title_dict = {}
    id_num = 0
    with open(titles_file) as titles:
        title = titles.readline()
        while title:
            id_title_dict[id_num] = title
            # if id_num % 10000000 == 0:
            #     pickle.dump(id_title_dict, open('data/titles_' + str(id_num), 'wb'))
            title = titles.readline()
            id_num += 1
    return id_title_dict

def build_outlinks_graph(links_file):
    '''
    Returns dictionary of id to list of ids that outlink from that artcile
    links_file: text file of link_id: outlinks (line-by-line)
    '''
    id_outlinks_dict = {}
    count = 0
    with open(links_file) as links:
        link = links.readline()
        while link:
            id_to_links = link.split(':')
            id_num, outlinks = int(id_to_links[0]), id_to_links[1]
            outlinks = [int(outlink) for outlink in outlinks.split()]
            id_outlinks_dict[id_num] = outlinks
            if count % 100000 == 0:
                print(count)
                # pickle.dump(id_outlinks_dict, open('data/outlinks_' + str(count), 'wb'))
            link = links.readline()
            count += 1
    return id_outlinks_dict

if __name__ == '__main__':
    print('Processing titles...')
    id_title_dict = build_id_title_dict('titles-sorted.txt')
    pickle.dump(id_title_dict, open('data/titles.txt', 'wb'))
    print('Processing outlinks...')
    id_outlinks_dict = build_outlinks_graph('links-simple-sorted.txt')
    pickle.dump(id_outlinks_dict, open('data/outlinks.txt', 'wb'))
