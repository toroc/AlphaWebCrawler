from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urljoin
from urllib.parse import urlparse

import re
import html5lib


def html_parser(url, keyword):
    title = ''
    try:
        response = urlopen(url)
    except:
        return {'title': '',
                'urls': [],
                'keyword_found': False}
    html = response.read()
    soup = BeautifulSoup(html, "html5lib")
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
        urls.append(finalLink)

    return {'title': title,
            'urls': urls,
            'keyword_found': keyword_found}
