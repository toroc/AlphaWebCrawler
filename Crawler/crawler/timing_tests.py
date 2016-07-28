import time
import sys

from link_visitor import web_crawler


TOTAL_TESTS = 5

out_file = "time_tests.txt"
output = open(out_file, "w")

for i in range(TOTAL_TESTS):
	test_num = "Test #" + str(i)
	output.write(test_num)
	start_overall = time.clock()
	output.write(web_crawler('http://www.oregonstate.edu','Carol', False))
	end_overall = time.clock()
	elapsed_overall= end_overall - start_overall
	output.write("dfs_crawl:\t", elapsed_overall)
	#print(results)

output.close