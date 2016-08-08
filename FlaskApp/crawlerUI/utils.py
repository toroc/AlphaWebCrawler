from flask import request

def parse_multidict(request_form):
    """Converts Flask form data to standard dictionary.

    :param request_form: The POST request body from a Flask request object.
    :returns: Python dictionary containing the POST form data.
    """

    data = {}
    data['url'] = request_form['url']
    data['limit'] = request_form['limit']
    data['keyword'] = request_form['keyword']
    data['crawl-type'] = request_form['crawl-type']
    return data

def is_bfs(request_form):
    """Determines whether or not the request is for a breadth-first search.

    :param request_form: The POST request body from a Flask request object.
    :returns: Boolean value as a string, for clientside JavaScript interpretation.
    """
    if request_form['crawl-type'] == "bfs":
        return "true"
    else:
        return "false"
