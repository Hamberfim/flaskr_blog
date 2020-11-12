# -*- coding: utf-8 -*-
"""
Program: test_factory.py
Created on 11/12/2020
@author: adhamlin

This program makes test using fixtures in conftest.py by
Matching the function names with the names of arguments in these test functions
"""
# imports
from flaskr import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World!  The Flask App is Running.'
