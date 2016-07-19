"""
The flask application package.
"""
import logging
from flask import Flask, current_app, redirect, url_for, session, Blueprint
import config


def create_app(config, debug=False, testing=False, config_overrides=None):
    app = Flask(__name__)
    app.config.from_object(config)

    app.debug = debug
    app.testing = testing

    if config_overrides:
        app.config.update(config_overrides)

    # Configure logging
    if not app.testing:
        logging.basicConfig(level=logging.INFO)

    # # Setup the data model.
    # with app.app_context():
    #     model = get_model()
    #     model.init_app(app)

    #app.register_blueprint(Crawler.crawler)
    return app

#app = create_app(config)
# def get_model():
#     model_backend = current_app.config['DATA_BACKEND']
#     if model_backend == 'cloudsql':
#         from . import model_cloudsql
#         model = model_cloudsql
#     elif model_backend == 'datastore':
#         from . import model_datastore
#         model = model_datastore
#     elif model_backend == 'mongodb':
#         from . import model_mongodb
#         model = model_mongodb
#     else:
#         raise ValueError(
#             "No appropriate databackend configured. "
#             "Please specify datastore, cloudsql, or mongodb")

#     return model
app = create_app(config)

# from crawlerUI.Crawler.views import mod as crawler_module
# app.register_blueprint(crawler_module)

import views