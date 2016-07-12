from flask import Blueprint, request, session, redirect, url_for, render_template, Response, jsonify
from crawlerUI.Crawler.link_visitor import link_visitor

mod = Blueprint('crawler', __name__, url_prefix='/crawler')

@mod.route('/', methods=['GET', 'POST'])
def crawler():
    error = None
    if request.method == 'POST':
        start_url = request.form['url']
        crawl_type = request.form['crawl-type']
        keyword = request.form['keyword']
        limit = request.form['limit']
        limit = int(limit)
 	

        if crawl_type == "dfs":
            results = link_visitor(start_url, True, keyword, limit)
        else:
            results = link_visitor(start_url, False, keyword, limit)
        
        

        resp = jsonify(results)
        resp.status_code = 200
        return resp


