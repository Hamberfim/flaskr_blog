# -*- coding: utf-8 -*-
"""
Program: conftest.py
Created on 11/12/2020
@author: adhamlin

PyTesting - Pytest uses fixtures by matching their function names with the names of arguments in the test functions
This program creates fixture setup functions that each test will use
"""
# imports
import os
import tempfile
import pytest
from flaskr import create_app
from flaskr.db import get_db
from flaskr.db import init_db


with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    """
    tempfile.mkstemp() creates and opens a temporary file, returning the file object and the path to it,
    overriding the original db path with a temporary path instead of the instance folder where the original db is
    """
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,  # app is in testing mode
        'DATABASE': db_path,  # temporary path
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """
    Calls the app.test_client() with the application object created by the app fixture above
    Tests will use this client to make requests to the application without running the server
    :param app:
    :return:
    """
    return app.test_client()


@pytest.fixture
def runner(app):
    """
    creates a runner that can call the Click commands registered with the application
    :param app:
    :return:
    """
    return app.test_cli_runner()


# most of the views require a user to be logged in
class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)
