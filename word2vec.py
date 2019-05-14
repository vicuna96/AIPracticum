from game import *
from similarity_algs import *
#import threading

if __name__ == '__main__':
    #source2 = random_id_generator(id_attrib_dict)
    #source1 = title_to_id['Machine learning']
    #target2 = random_id_generator(id_attrib_dict)
    #target1 = title_to_id['Battle of the Atlantic']
    #paths = [('Jesus', 'Volkswagen'), ('Toothpaste', 'William Shakespeare'), ('Puppy', 'Racism'), ('Pants', 'Shirt'), ('Elmo', 'Teletubbies'), 
    paths = [('Apple pie', 'Rock (geology)'), ('Here', 'There'), ('Oboe', 'Veto'), ('Satyr', 'Wombat'), ('Locust', 'Bicycle')]

    metric = lambda target : get_word2vec(id_attrib_dict, target)

    game = lambda source, target : priority_beam_search(source, target, 10, metric(target), optional={'tfs': tfs, 'id_to_row': id_to_row})

    for source, target in paths:
        print(source, target)
        source_id = title_to_id[source]
        target_id = title_to_id[target]
        game(source_id, target_id)
