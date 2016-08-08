"""
Routes and views for the flask application.
"""
from crawlerUI import app
from datetime import datetime
from flask import render_template, request, Markup
import requests
import json
from utils import parse_multidict, is_bfs

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/crawl', methods=['GET'])
def crawl():
    """Renders the crawl request page."""
    return render_template(
        'crawl.html',
        title='Crawl',
        year=datetime.now().year,
        message='The crawl page.'
    )


@app.route('/crawl', methods=['POST'])
def visualize_crawl():
    form_data = parse_multidict(request.form)
    crawl_request = requests.post("http://alpha-crawler.appspot.com/", data=form_data, timeout=10.0)
    return render_template(
        'visualizer.html',
        title='Crawled by Post',
        year=datetime.now().year,
        message='The crawl page after a post.',
        response=json.dumps(crawl_request.json(), ensure_ascii=False),
        bfs=is_bfs(form_data)
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.',
        message2='Dev Team'
    )
# Add an error handler. This is useful for debugging the live application,
# however, you should disable the output of the exception for production
# applications.




@app.errorhandler(500)
def server_error(e):
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500
