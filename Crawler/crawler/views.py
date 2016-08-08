
from crawler.link_visitor import web_crawler
from crawler import app
from datetime import datetime
from flask import render_template, request, Response, jsonify
import logging

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
     	  
            limit = validate_limit(limit)

            if crawl_type == "dfs":
                results = web_crawler(start_url, True, keyword, limit)
            else:
                results = web_crawler(start_url, False, keyword, limit)
            
            return validate_results(results)

        else:
            return missing_params()

    else:
        if 'url' in request.args and 'crawl-type' in request.args:
            start_url = request.args['url']
            crawl_type = request.args['crawl-type']
            keyword = request.args['keyword']
            limit = request.args['limit']
            limit = int(limit)
        
            limit = validate_limit(limit)
            
            if crawl_type == "dfs":
                results = web_crawler(start_url, True, keyword, limit)
            else:
                results = web_crawler(start_url, False, keyword, limit)
            
            return validate_results(results)
           
        else:
            return missing_params()


def missing_params():
    response = jsonify({'code': 422,'message': 'Missing required parameters: url, crawl-type'})
    response.status_code = 422
    return response

def invalid_start_page():
    response = jsonify({'code': 422, 'message': 'Invalid start page.' })
    response.status_code = 422
    return response

def validate_results(results):
    logging.warn(results)
    if results:
        resp = jsonify(results)
        resp.status_code = 200
        return resp
    else:
        return invalid_start_page()

def validate_limit(limit):
    if limit > 20:
        return 20
    else:
        return limit

@app.errorhandler(500)
def server_error(e):
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500