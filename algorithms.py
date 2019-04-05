from article import Article

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

