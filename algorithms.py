from article import Article

folder = '/mnt/c/Users/danis_000/word2vec/'
word2vec = 'GoogleNews-vectors-negative300.bin'

def spacy_small_sim(text1, text2):
    import spacy
    nlp = spacy.load("en_core_web_sm")
    return nlp(text1).similarity(nlp(text2))

def word2vec_sim(text1, text2):
    import gensim
    model = gensim.models.KeyedVectors.load_word2vec_format(folder+word2vec, binary=True)
    return model.wv.n_similarity(text1.split(" "), text2.split(" "))

'''
Performs depth-first search only up to [maxDepth] from
[currentNode] without revisiting nodes in the set [visited], 
and returns True if [targetId] is found, False otherwise. 
'''
def dl_dfs(currentNode, targetId, maxDepth, visited):
    # If at the target, return True
    if currentNode.getId() == targetId:
        return True
    # If at maxDepth, return False
    if maxDepth <= 0:
        return False
    # Search over the next layer/depth
    for link in currentNode.getOutLinks():
        if link.getId() not in visited:
            visited.add(link.getId())
            if dl_dfs(link, targetId, maxDepth - 1, visited):
                return True
    return False


'''
Performs iterative deepening depth-first search from 
[sourceNode] up to [maxDepth] and returns True iff it finds
the Article node that corresponds to [targetId] 
'''
def itdeep_search(sourceNode, targetId, maxDepth):
    for depth in range(maxDepth):
        visited = set()
        if (dl_dfs(sourceNode, targetId, depth, visited)):
            return True
    return False

def beam_search(sourceNode, targetId, maxDepth):
    return

'''
Greedily searches for article with [targetTitle] by a DFS approach
that chooses the article that contains a word that is most similar
to the [targetTitle], where similarity is measured by 
    [measure]: (title,title) -> x \in [0,1]
The algorithm will make at most [maxDepth] transitions, or will run forever if
[maxDepth] == None
'''
def greedy_similarity_search(sourceNode, targetTitle, measure, maxDepth=1000):
    visited = set()
    allDepths = (maxDepth == None)
    depth = 0
    while allDepths or (depth < maxDepth):
        newLink, maxSim = None, 0.0
        for link in sourceNode.getOutLinks():
            if link.getTitle == targetTitle:
                return link
            if link.getId() not in visited:
                sim = measure(link.getTitle(), targetTitle)
                if sim > maxSim:
                    maxSim, newLink = sim, link
        depth += 1
        if newLink == None:
            return None
        else:
            visited.add(newLink.getTitle())
    return None





'''
Adds all the articles at depth [maxDepth] or less from 
the manually created [sourceNode] into the set [visited].
Used to construct a set of articles reachable from [sourceNode]
without creating the whole graph for Wikipedia.

NOTE: The implementation is clearly naive, and will likely
be improved once we know how we will be storing the data.
'''
def id_graphBuild(sourceNode, maxDepth, visited):
    # If at maxDepth, return False
    if maxDepth <= 0:
        return
    # Search over the next layer/depth
    for link in sourceNode.getOutLinks():
        newNode = createArticle(link)
        visited.add(newNode)
        # Create an article would be a function that
        # creates an [Article] object from whatever structure
        # we are using to store the article
        id_graphBuild(newNode, maxDepth - 1, visited)

    return visited

