import sys
from htmlParser import parse_html
import urllib

result = parse_html(sys.argv[1], sys.argv[2])
print(result['title'])
print(result['keyword_found'])
print(result['urls'])
