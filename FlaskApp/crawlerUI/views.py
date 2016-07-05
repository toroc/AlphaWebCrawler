"""
Routes and views for the flask application.
"""
from crawlerUI import app
from datetime import datetime
from flask import render_template


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/crawl')
def crawl():
    """Renders the contact page."""
    return render_template(
        'crawl.html',
        title='Crawl',
        year=datetime.now().year,
        message='The crawl page.'
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