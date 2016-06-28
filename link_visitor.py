from page_class import *
import random
import queue
import time
import pprint
import logging
random.seed(time.time())
urls = [
        'http://www.stackoverflow.com/',
        'http://stackoverflow.com/',
        'http://google.com/',
        'http://bing.com'
    ]

def html_parser(url, keyword=None):

    return "Page Title", urls , False

def rand_visiting(urls):

    total_urls = len(urls)
    rand_idx = random.randrange(0,total_urls)

    rand_url = urls[rand_idx]
    #rand_url = rand_obj['url']
    logging.warn(rand_url)

    return rand_url

def link_visitor(url, keyword=None, limit=10, DFS=True):
    """"""
    page_urls = list()
    page_list = list()
    visited_urls = set()
    url_q = queue.Queue()
    url_q.put(url)


    # Add starting URL to queue
    title, page_urls, kwd_found = html_parser(url, keyword)
    start_page = web_page(url, title, None)
    #url_q.put(start_page['url'])
    url_q.put(start_page.url)

    while not url_q.empty() and limit >0:

        url = url_q.get()

        if url not in visited_urls:
            # Get page title and urls on page
            title,page_urls, kwd_found = html_parser(url, keyword)
            if kwd_found:
                # Done
                pass
            visited_urls.add(url)    
            cur_page = web_page(url, title, None)
            page_list.append(cur_page.asDict)
        # Call DFS/BFS based on input
            #print(page_urls)
            next_url = rand_visiting(page_urls)
            url_q.put(next_url)
            limit -=1

    print(page_list)

    """page_list contains visited URLS"""
    # Return results

    # Create page objects for the URL only when visited
    # for x in page_urls:
    #     logging.warn(x)
    #     # Set the page url and parent
    #     temp_page = web_page(x, None, url)
    #     logging.warn(temp_page)
    #     # Convert to dictionary
    #     page_list.append(temp_page.__dict__)
    #     url_q.put(temp_page.__dict__)

    # logging.warn(page_list)
    # logging.warn(url_q)
    # pp = pprint.PrettyPrinter(indent=4)
    # pprint.saferepr(page_list)

    #url_q = queue.Queue()
    

    


link_visitor('test')


