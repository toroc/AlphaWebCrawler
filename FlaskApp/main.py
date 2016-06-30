import crawlerUI
from crawlerUI import app
import config
import os, sys
# Add the parent directory to the path
# CURRENTDIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
# if CURRENTDIR not in sys.path:
#     sys.path.append(CURRENTDIR)





"""Used for running site locally"""

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8080, debug=True)