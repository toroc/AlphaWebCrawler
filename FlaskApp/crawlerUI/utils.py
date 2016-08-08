from flask import request

def parse_multidict(request_form):
    """Converts Flask form data to standard dictionary.

    :param request_form: The POST request body from a Flask request object.
    """

    data = {}
    data['url'] = request_form['url']
    data['limit'] = request_form['limit']
    data['keyword'] = request_form['keyword']
    data['crawl-type'] = request_form['crawl-type']
    return data
