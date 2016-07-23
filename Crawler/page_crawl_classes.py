import Queue




class WebPage(object):
    """Object maintaining details of visited page."""
    def __init__(self, url, title, parent, children, kwd_found, visited):
        self.url = url
        self.title = title
        self.parent = parent
        self.children = children
        self.children_count = len(children)
        self.has_keyword = kwd_found
        self.visited = visited

    
    def as_dict(self):
        return self.__dict__
        #print(d)
        #return d
    def page_info(self):
        return self.as_dict()


class Pages(object):
    """Object maintaining list of visited pages."""
    def __init__(self):
        self.visited = list()
    
    def as_dict(self):
        return self.__dict__

    def track(self, web_page_obj):
        return self.visited.append(web_page_obj)

    
    def show(self):
        return self.as_dict

    def visit_count(self):
        return len(self.visited)
    



    
class CrawlOptions(object):
    """Object maintaining options for current crawl."""
    def __init__(self, limit=10, keyword=None):
        self.limit = limit
        self.keyword = keyword
        self.kwd_found = False

    def lower(self):
        self.limit -= 1

    
    def cur_limit(self):
        return self.limit


class Crawl(object):
    """Object maintaining details of entire crawl."""
    def __init__(self, url, limit, keyword):
        self.start = url
        self.url_q = Queue.Queue()
        self.visited_set = set()
        self.options = CrawlOptions(limit, keyword)
        self.data = Pages()
        

    def met_limit(self):
        return self.options.cur_limit() > 1
    
    def dequeue(self):
        return self.url_q.get()
    
    
    def enqueue(self, url):
        return self.url_q.put(url)
   
   
    def empty_q(self):
        return self.url_q.empty()
    
    
    def add_set(self, url):
        return self.visited_set.add(url)

    
    def track_data(self, page):
        self.data.track(page)

    def show_data(self):
        return self.data.as_dict()
     #return self.data.track(page.as_dict)