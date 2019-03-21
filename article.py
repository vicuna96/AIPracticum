class Article(object):
    """ A Wikipedia Article.

    Attributes:
        __url [string]:             the url of the article
        __outLinks[article list]:   all the articles mentioned in the current article
        __contents[string]:         The text contained in the Wikipedia article
        __topWords[string list]     A list of the most meaningful words using the [] metric
    """

    def __init__(self, link, hyperlinks, contents, topWords):
        """Return a new Article object."""
        self.__url = link
        self.__hyperlinks = hyperlinks
        self.__contents = contents
        self.__topWords = topWords

    def getUrl(self):
        """ Returns the [url] where this Wikipedia article can be found. """
        return self.__url

    def getContents(self):
        """ Return the text contents of the this Wikipedia article. It should
            contain no hyperlinks. """
        return self.__contents

    def getOutLinks(self):
        """ Returns a list of Articles that are linked to in this article through hyperlinks."""
        return self.__outLinks

