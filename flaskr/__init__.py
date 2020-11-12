# -*- coding: utf-8 -*-
"""
Program: __init__.py
Created on 11/11/2020
@author: adhamlin

This is the application factory and it tells Python that the 'flaskr' directory should be treated as a package.
source: https://flask.palletsprojects.com/en/1.1.x/tutorial/
"""
# imports
import os
from flask import Flask


def create_app(test_config=None):
    """
    Application Factory Function:
    Any configuration, registration or other setup the application needs will happen inside this function.
    :param test_config:
    :return: the application

    Run your Application:
    windows - at the powershell prompt> '$env:FLASK_APP = "flaskr"'
    windows - at the powershell prompt> '$env:FLASK_ENV = "development"'
    windows - at the powershell prompt> 'flask run'
    ----------------------------------------------
    windows - at the cmd prompt> 'set FLASK_APP=flaskr'
    windows - at the cmd prompt> 'set FLASK_ENV=development'
    windows - at the cmd prompt> 'flask run'
    ----------------------------------------------
    linux/mac - at the terminal> 'export FLASK_APP=flaskr'
    linux/mac - at the terminal> 'export FLASK_ENV=development'
    linux/mac - at the terminal> 'flask run'
    """
    # create and configure the flask instance
    app = Flask(__name__, instance_relative_config=True)  # configuration files are relative to the instance folder
    app.config.from_mapping(  # sets some default configuration
        SECRET_KEY='dev',  # this should be overridden with a random value when deploying
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),  # path to the SQLite db file
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        # override default config with values taken from config.py
        # in the instance folder if exists. I.E., used to set a real SECRET_KEY
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)  # so the tests can be configured independently of any development values

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)  # ensures that app.instance_path exists
    except OSError:
        pass

    # a simple page that says hello - a simple route so you can see the application is working
    @app.route('/hello')
    def hello():
        """
        creates a simple route so you can see the application working
        :return:
        """
        return 'Hello, World!  The Flask App is Running.'

    # Import and call init_app functions from db.py
    from . import db
    db.init_app(app)

    # Import and register the auth blueprint from auth.py
    # the auth has views to register new users and to log in and log out
    from . import auth
    app.register_blueprint(auth.bp)

    # Import and register the blog blueprint from blog.py
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
