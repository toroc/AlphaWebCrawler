from bs4 import BeautifulSoup


def parse_html(page):
    soup = BeautifulSoup(page, "html5lib")
    for link in soup.find_all('a'):
        print(link.get('href'))