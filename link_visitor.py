from page_class import *
import pprint

urls = [
        'http://www.stackoverflow.com/questions/5331266/python-easiest-way-to-scrape-text-from-list-of-urls-using-beautifulsoup',
        'http://stackoverflow.com/questions/5330248/how-to-rewrite-a-recursive-function-to-use-a-loop-instead'
    ]

def html_parser(url, keyword=None):

    return "Page Title", urls


def link_visitor(url, keyword, limit=20, DFS=True):
    """"""

    page_urls = list()

    # Get page title and urls on page
    title, page_urls = html_parser(url)

    # Create page object
    cur_page = web_page(url, title, None)
    print(cur_page.url)

    page_list = list()

    # Create page objects for each url in list
    for x in page_urls:
        print(x)
        # Set the page url and parent
        temp_page = web_page(x, None, url)
        print(temp_page)
        # Convert to dictionary
        page_list.append(temp_page.__dict__)

    print(page_list)
    pp = pprint.PrettyPrinter(indent=4)
    pprint.saferepr(page_list)


    # Call DFS/BFS based on input



    # Return results
    

link_visitor('test')
