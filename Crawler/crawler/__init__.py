"""
The flask application package.
"""
import logging
from flask import Flask, current_app, redirect, url_for, session, Blueprint


def create_app():
    app = Flask(__name__)
    
    return app

app = create_app()

# from crawler.views import mod as crawler_module
# app.register_blueprint(crawler_module)

#from crawler import views