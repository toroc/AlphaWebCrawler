from page_class import *
import random
import queue
import time
import pprint
import logging
random.seed(time.time())


urls = ['http://www.stackoverflow.com/',
        'http://stackoverflow.com/',
        'http://google.com/',
        'http://bing.com']

def html_parser(url, keyword=None):

    return "Page Title", urls , False

def rand_visiting(urls):

    total_urls = len(urls)
    rand_idx = random.randrange(0,total_urls)

    rand_url = urls[rand_idx]
    #rand_url = rand_obj['url']
    #logging.warn(rand_url)

    return rand_url

def link_visitor(url, keyword=None, limit=10, DFS=True):
    """"""
    #Set uo crawl class object
    crawl = crawl_class(url,limit, keyword)
    


    #Set up the start page
    start_page = visit(url,None, crawl.options)

    #Add Start page to QUE

    crawl.url_q.put(start_page.url)
    crawl.visited_set.add(start_page.url)
    crawl.pages.visited.append(start_page.asDict)
    if DFS:
        dfs_crawl(crawl, start_page)

    print(crawl.pages.visited)



def dfs_crawl(crawling, start_page):
    neighbors = start_page.neighbors
    from_page = start_page.url
    
    
    while not crawling.url_q.empty() and crawling.options.limit > 0:
        url = crawling.url_q.get()

        next_url = rand_visiting(neighbors)

        if next_url not in crawling.visited_set:
            crawling.url_q.put(next_url)           
        

        if url not in crawling.visited_set:
            # Get page title and urls on page
            cur_page = visit(url, from_page, crawling.options)
            from_page = cur_page.url
            neighbors = cur_page.neighbors
            crawling.visited_set.add(url)
            crawling.pages.visited.append(cur_page.asDict)
            
            crawling.options.limit -=1

            if crawling.options.kwd_found:
                # Done
                break
       
        


    print("Done with the crawl")
    logging.warn("Done with dfs crawl")
   


def bfs_crawl(options, start_page, visited_list, url_queue):

    #add all neighbors to the the queue
    neighbors = start_page.neighbors
    for x in neighbors: 
        url_queue.put(x)

    #while there are unvisited neighbors
def visit(url, from_page=None, options=None):

     title, page_urls, kwd_found = html_parser(url, options.keyword)
     cur_page = web_page(url, title, from_page, page_urls)
     options.kwd_found = kwd_found
     
     return cur_page

link_visitor('test')


