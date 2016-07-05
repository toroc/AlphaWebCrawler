"""This is the link visitor module.

This module handles the page crawls.
(Will add more details)
"""

from page_crawl_classes import *
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
    """Return page title, urls on page, and keyword found """

    return "Page Title", urls , False



def rand_visiting(urls):
    """Return a random url to visit."""
    total_urls = len(urls)
    rand_idx = random.randrange(0,total_urls)

    rand_url = urls[rand_idx]
    #logging.warn(rand_url)

    return rand_url

def link_visitor(url, keyword=None, limit=10, DFS=True):
    """Return and run the crawl."""
    #Set uo crawl class object
    
    crawl = Crawl(url, limit, keyword)
    
    
    #Set up the start page
    start_page = visit(url,None, crawl.options)

    #Add Start page to queue and set
    crawl.enqueue(url)

    crawl.addSet(url)

    crawl.data.track(start_page.page_info())

    if DFS:
        dfs_crawl(crawl, start_page)
    else:
        bfs_crawl(crawl, start_page)


   #print(crawl.data.visited)

    print(crawl.data.as_dict())

    



def dfs_crawl(crawling, start_page):
    """Update crawling with results of dfs crawl."""

    children = start_page.children
    from_page = start_page.url
    
    
    while not crawling.emptyQ() and crawling.options.met_limit():
        url = crawling.dequeue()

        next_url = rand_visiting(children)

        if next_url not in crawling.visited_set:
            crawling.enqueue(next_url)         
        

        if url not in crawling.visited_set:
            # Get page title and urls on page
            cur_page = visit(url, from_page, crawling.options)
            from_page = cur_page.url
            children = cur_page.children
            #crawling.visited_set.add(url)
            crawling.addSet(url)
            #crawling.pages.visited.append(cur_page.as_dict)
            #crawling.track_data(cur_page.as_dict)
            crawling.data.track(cur_page.page_info())
            
            #crawling.options.limit -=1
            crawling.options.lower()

            if crawling.options.kwd_found:
                # Done
                break

    logging.warn("Done with dfs crawl")
   


def bfs_crawl(options, start_page, visited_list, url_queue):

    #add all children to the the queue
    children = start_page.children
    for x in children: 
        url_queue.put(x)

    #while there are unvisited children
def visit(url, from_page=None, options=None):
    """Return new page object with details of page visited."""

    title, page_urls, kwd_found = html_parser(url, options.keyword)
    cur_page = WebPage(url, title, from_page, page_urls)
    options.kwd_found = kwd_found
     
    return cur_page



link_visitor('test')


