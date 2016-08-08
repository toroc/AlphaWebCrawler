from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urljoin
from urllib.parse import urlparse

import re
import lxml
import socket
import requests

timeout = 10
socket.setdefaulttimeout(timeout)


from lxml import html


def html_parser(url, keyword):
    title = ''
    try:
        response = requests.get(url)
    except:
        return {'title': '',
                'urls': [],
                'keyword_found': False,
                'visited': False}
    #html = response.read()
    soup = BeautifulSoup(response.content, "lxml")
    title_tag = soup.title
    if (title_tag):
        title = title_tag.string

    keyword_found = False

    if (keyword):
        keyword_result = soup.find_all(string=re.compile(keyword), limit=1)
        if len(keyword_result) > 0:
            keyword_found = True

    urls = []
    for link in soup.find_all('a'):
        currentLink = link.get('href')
        linkTest = urlparse(currentLink)
        if linkTest.scheme and linkTest.netloc:
            finalLink = currentLink
        else:
            finalLink = urljoin(url, currentLink)

        if finalLink.startswith('http'):
            urls.append(finalLink)

    return {'title': title,
            'urls': urls,
            'keyword_found': keyword_found,
            'visited': True}



def improved_parser(url, keyword):
    """Better performing parser"""
    title = ''
    try:
        response = requests.get(url)
    except:
        return {'title': '',
                'urls': [],
                'keyword_found': False,
                'visited': False}

    #tree = html.fromstring(response.content)
    soup = BeautifulSoup(response.content, "lxml")
    parsed_content = html.fromstring(response.content)
    #title_tag = soup.title
    title_tag = parsed_content.xpath('//title/text()')
    if (title_tag):
        title = str(title_tag)

    keyword_found = False

    if (keyword):
        if soup.body.find(text = re.compile(keyword)):
            # Keyword exists in the document body
            keyword_found = True


    # Get only valid http URLs
    urls = get_http_links(response, parsed_content)

    return {'title': title,
            'urls': urls,
            'keyword_found': keyword_found,
            'visited': True}


def get_http_links(response, parsed_content):
    """Return only http links."""
    #print("getting only http links")
    page_links = []
    # extract only links that begin with http
    links = {urljoin(response.url, url) for url in parsed_content.xpath('//a/@href') if urljoin(response.url, url).startswith('http')}


    for link in links:
        #Add only links that haven't been already added to the set
        if link not in page_links:
            page_links.append(link)

    return page_links