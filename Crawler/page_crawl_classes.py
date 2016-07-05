import queue




class WebPage(object):
    """Object maintaining details of visited page."""
    def __init__(self, url, title, parent, children):
        self.url = url
        self.title = title
        self.parent = parent
        self.children = children

    
    def asDict(self):
        return self.__dict__
        #print(d)
        #return d
    def page_info(self):
        return self.asDict()


class Pages(object):
    """Object maintaining list of visited pages."""
    def __init__(self):
        self.visited = list()
    
    def asDict(self):
        return self.__dict__

    def track(self, web_page_obj):
        return self.visited.append(web_page_obj)

    
    def show(self):
        return self.asDict
    



    
class CrawlOptions(object):
    """Object maintaining options for current crawl."""
    def __init__(self, limit=10, keyword=None):
        self.limit = limit
        self.keyword = keyword
        self.kwd_found = False

    def lower(self):
        self.limit -= self.limit

    
    def metLimit(self):
        return self.limit > 0


class Crawl(object):
    """Object maintaining details of entire crawl."""
    def __init__(self, url, limit, keyword):
        self.start = url
        self.url_q = queue.Queue()
        self.visited_set = set()
        self.options = CrawlOptions(limit, keyword)
        self.data = Pages()
        

    
    def dequeue(self):
        return self.url_q.get()
    
    
    def enqueue(self, url):
        return self.url_q.put(url)
   
   
    def emptyQ(self):
        return self.url_q.empty()
    
    
    def addSet(self, url):
        return self.visited_set.add(url)

    
    def track_data(self, page):
        self.data.track(page)

    def show_data(self):
        return self.data.asDict()
     #return self.data.track(page.asDict)