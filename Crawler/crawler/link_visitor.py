"""This is the link visitor module.

This module handles the page crawls.
(Will add more details)
"""


from crawler.page_crawl_classes import *
import urllib
import random
import queue
import time
import pprint
import logging
import crawler.html_parser as hp
random.seed(time.time())
import time




def rand_visiting(urls=[]):
    """Return a random url to visit."""
    #logging.warn(urls)
    total_urls = len(urls)
    #logging.warn(total_urls)
    rand_idx = random.randrange(0,total_urls)

    rand_url = urls[rand_idx]
    #logging.warn(rand_url)

    return rand_url

def web_crawler(url, DFS=True, keyword=None, limit=10, ):
    """Return results from running crawl."""
    #Set up crawl class object
    crawl = Crawl(url, limit, keyword)
    
    #Set up the start page
    start_page = visit(url, None, crawl.options)

    #Add Start page to queue and set
    crawl.enqueue(url)

    crawl.add_set(url)

    crawl.data.track(start_page.page_info())

    logging.warn(start_page.visited)
    if start_page.visited:
        if not start_page.has_keyword:
            #Keyword not found continue

            if DFS:
                dfs_crawl(crawl, start_page)
            else:
                bfs_crawl(crawl, start_page)
    else:
        #Invalid start page
        return False
    #print(crawl.data.as_dict())
    #pp.pprint(crawl.data.as_dict())
    #pp.pprint(crawl.data.visit_count())
    return crawl.data.as_dict()


   
def dfs_crawl(crawling, start_page):
    """Update crawling with results of dfs crawl."""

    children = crawling.options.get_children()

    from_page = start_page.url

    url = rand_visiting(children)

    while crawling.met_limit():

        
       
        if url not in crawling.visited_set:
            prev_from = from_page
            prev_children = children
            
            cur_page = visit(url, from_page, crawling.options)


            
            num_kids = len(crawling.options.get_children())
            if cur_page.visited:

                if num_kids == 0:
                    from_page = prev_from
                    children = prev_children
                else:
                    children = crawling.options.get_children()
                    from_page = cur_page.url

            crawling.add_set(url)

            crawling.data.track(cur_page.page_info())
            
            #crawling.options.limit -=1
            crawling.options.lower()

            if crawling.options.kwd_found:
                # Done
                logging.debug("Found keyword")
                break

            url = rand_visiting(children)


def bfs_crawl(crawling, start_page):
    """Update crawling with results of bfs crawl."""
    children = crawling.options.get_children()
    from_page = start_page.url
    
    while not crawling.empty_q() and crawling.met_limit():

        u = crawling.dequeue()

        if u not in crawling.visited_set:

            cur_page = visit(u, from_page, crawling.options)

            if cur_page.visited:
                children = crawling.options.get_children()
                from_page = u

            crawling.data.track(cur_page.page_info())
            crawling.options.lower()
            


        for x in children:
            if x not in crawling.visited_set:
                crawling.enqueue(x)
        

        if crawling.options.kwd_found:
            # Done
            logging.debug("Found keyword")
            break

    logging.debug("Done with bfs crawl")


def visit(url, from_page=None, options=None):
    """Return new page object with details of page."""

    results = hp.improved_parser(url, options.keyword)
    cur_page = WebPage(url, results['title'], from_page, results['keyword_found'], results['visited'])
    options.kwd_found = results['keyword_found']
    options.set_children(results['urls'])
     
    return cur_page
