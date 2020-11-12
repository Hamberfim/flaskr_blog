# -*- coding: utf-8 -*-
"""
Program: test_db.py
Created on 11/12/2020
@author: adhamlin

Testing db for pytests.
"""
# imports
import sqlite3
import pytest
from flaskr.db import get_db


def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed' in str(e.value)


def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    # monkeypatch fixture to replace the init_db function
    # runner fixture in 'conftest.py' is used to call the init-db command by name
    monkeypatch.setattr('flaskr.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called
