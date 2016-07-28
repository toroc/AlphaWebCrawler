import time
import sys

from local_crawler import web_crawler


start_overall = time.clock()
results = web_crawler('http://www.oregonstate.edu','Carol', False)
end_overall = time.clock()
elapsed_overall= end_overall - start_overall
print("bfs_crawl:\t", elapsed_overall)
#print(results)