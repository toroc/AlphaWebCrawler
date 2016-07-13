from crawlerUI import app, views
import config
import os, sys

rootdir = os.path.dirname(os.path.abspath(__file__))
lib = os.path.join(rootdir, 'lib')
sys.path.append(lib)

# Add the parent directory to the path
# CURRENTDIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
# if CURRENTDIR not in sys.path:
#     sys.path.append(CURRENTDIR)

"""Used for running site locally"""

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8080, debug=True)