import queue
class page_class(object):
    """description of class"""


class web_page:
    """docstring for web_page"""
    def __init__(self, url, title, parent, neighbors):
        self.url = url
        self.title = title
        self.parent = parent
        self.neighbors = neighbors


    @property
    def asDict(self):
        d = self.__dict__
        #print(d)
        return d


class pages:
    def __init__(self):
        self.visited = list()

    @property
    def add_visited(self, page):
        return self.visited.add(page)
    


    
class crawl_options:
    def __init__(self, limit=10, keyword=None):
        self.limit = limit
        self.keyword = keyword
        self.kwd_found = False


class crawl_class:
    def __init__(self, url, limit, keyword):
        self.start = url
        self.options = crawl_options(limit, keyword)
        self.pages = pages()
        self.url_q = queue.Queue()
        self.visited_set = set()

    @property
    def dequeue(self):
        return self.url_q.get()

    @property
    def enqueue(self, url):
        return self.url_q.put(url)

    @property
    def addSet(self, url):
        return self.visited_set.add(url)
    
    
    
    