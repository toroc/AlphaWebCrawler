AlphaWebCrawler HTML Parser

Dependencies: BeautifulSoup4, html5lib

Advantages: BeautifulSoup4 makes the page into a data structure that is very easily accessible.
	    html5lib uses Python

Disadvantages: html5lib is the slowest of the parsing options

Returns a dictionary with a 'title', 'keyword_found', and 'urls'