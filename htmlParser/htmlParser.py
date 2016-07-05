from bs4 import BeautifulSoup
from urllib.request import urlopen
import re


def parse_html(url, keyword):
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
    keyword_result = soup.find_all(string=re.compile(keyword), limit=1)
    if len(keyword_result) > 0:
        keyword_found= True
    else:
        keyword_found= False
    urls = []
    for link in soup.find_all('a'):
        urls.append(link.get('href'))

    return {'title': title,
            'urls': urls,
            'keyword_found': keyword_found}