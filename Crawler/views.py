
from crawler.link_visitor import web_crawler
from crawler import app
from datetime import datetime
from flask import render_template, request, Response, jsonify

@app.route('/', methods=['GET', 'POST'])
def crawler():
    error = None
    if request.method == 'POST':
        if request.form['url'] and request.form['crawl-type']:
            start_url = request.form['url']
            crawl_type = request.form['crawl-type']
            keyword = request.form['keyword']
            limit = request.form['limit']
            limit = int(limit)
     	

            if crawl_type == "dfs":
                results = web_crawler(start_url, True, keyword, limit)
            else:
                results = web_crawler(start_url, False, keyword, limit)
            
            
            resp = jsonify(results)
            resp.status_code = 200
            return resp
        else:
            return not_found

    else:
        if 'url' in request.args and 'crawl-type' in request.args:
            start_url = request.args['url']
            crawl_type = request.args['crawl-type']
            keyword = request.args['keyword']
            limit = request.args['limit']
            limit = int(limit)
        

            if crawl_type == "dfs":
                results = web_crawler(start_url, True, keyword, limit)
            else:
                results = web_crawler(start_url, False, keyword, limit)
            
            
            resp = jsonify(results)
            resp.status_code = 200
            return resp
        else:
            return not_found()

def not_found():
    response = jsonify({'code': 422,'message': 'Missing parameters.'})
    response.status_code = 422
    return response

@app.errorhandler(500)
def server_error(e):
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500