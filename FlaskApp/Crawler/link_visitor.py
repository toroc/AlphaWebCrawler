"""This is the link visitor module.

This module handles the page crawls.
(Will add more details)
"""


from page_crawl_classes import *
import urllib
import random
import queue
import time
import pprint
import logging
import html_parser as hp
random.seed(time.time())

pp = pprint.PrettyPrinter(indent=4)

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

    crawl.add_set(url)

    crawl.data.track(start_page.page_info())

    if DFS:
        dfs_crawl_2(crawl, start_page)
    else:
        bfs_crawl(crawl, start_page)


   #print(crawl.data.visited)

    #print(crawl.data.as_dict())
    pp.pprint(crawl.data.as_dict())
    pp.pprint(crawl.data.visit_count())



    
def dfs_crawl_2(crawling,start_page):

    children = start_page.children

    from_page = start_page.url

    while crawling.options.met_limit():

        url = rand_visiting(children)

        if url not in crawling.visited_set:
            cur_page = visit(url, from_page, crawling.options)

            
            num_kids = cur_page.children_count

            if num_kids == 0:
                pass
            else:
                children = cur_page.children
                from_page = cur_page.url

            crawling.add_set(url)

            crawling.data.track(cur_page.page_info())
            
            #crawling.options.limit -=1
            crawling.options.lower()

            if crawling.options.kwd_found:
                # Done
                logging.warn("Found keyword")
                break


def dfs_crawl(crawling, start_page):
    """Update crawling with results of dfs crawl."""

    children = start_page.children
    from_page = start_page.url
    
    
    while not crawling.empty_q() and crawling.met_limit():
        url = crawling.dequeue()

        next_url = rand_visiting(children)

        if next_url not in crawling.visited_set:
            crawling.enqueue(next_url)         
        

        if url not in crawling.visited_set:
            # Get page title and urls on page
            cur_page = visit(url, from_page, crawling.options)
            
            num_kids = cur_page.children_count
            
            if num_kids == 0:
                next_url = rand_visiting(children)
                crawling.enqueue(next_url)
            else:
                children = cur_page.children
                from_page = cur_page.url
            

            
                # Go back to previous

            #crawling.visited_set.add(url)
            crawling.add_set(url)
            #crawling.pages.visited.append(cur_page.as_dict)
            #crawling.track_data(cur_page.as_dict)
            crawling.data.track(cur_page.page_info())
            
            #crawling.options.limit -=1
            crawling.options.lower()

            if crawling.options.kwd_found:
                # Done
                logging.warn("Found keyword")
                break

    logging.warn("Done with dfs crawl")
   


def bfs_crawl(crawling, start_page):

    from_page = None
    while not crawling.empty_q() and crawling.met_limit():

        u = crawling.dequeue()

        cur_page = visit(u, from_page, crawling.options)

        children = cur_page.children

        for x in children:
            if x not in crawling.visited_set:
                crawling.enqueue(x)


        crawling.data.track(cur_page.page_info())
        crawling.options.lower()
        from_page = u

        if crawling.options.kwd_found:
            # Done
            logging.warn("Found keyword")
            break

    logging.warn("Done with bfs crawl")

    #while there are unvisited children
def visit(url, from_page=None, options=None):
    """Return new page object with details of page visited."""

    results = hp.html_parser(url, options.keyword)
    cur_page = WebPage(url, results['title'], from_page, results['urls'])
    options.kwd_found = results['keyword_found']
     
    return cur_page



link_visitor('http://www.oregonstate.edu','Carol', 25, False)

