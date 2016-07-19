from flask import Blueprint, request, session, redirect, url_for, render_template, Response, jsonify
from crawlerUI.Crawler.link_visitor import web_crawler

mod = Blueprint('crawler', __name__, url_prefix='/crawler')

@mod.route('/', methods=['GET', 'POST'])
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
            resp.status_code = 422
            return resp

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

        resp.status_code = 422
        return resp



