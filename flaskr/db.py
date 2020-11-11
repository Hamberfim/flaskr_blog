# -*- coding: utf-8 -*-
"""
Program: db.py
Created on 11/11/2020
@author: adhamlin

Flask App stored db connection.
The connection is reused instead of creating a new connection if get_db is called a second time in the same request.
"""
# imports
import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    """
    'g' -is a unique object used to store data that might be accessed by multiple functions during the request
    :return:
    """
    if 'db' not in g:
        g.db = sqlite3.connect(  # establishes a connection
            current_app.config['DATABASE'],  # points to the Flask application handling the request
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row  # return rows that behave like dicts

    return g.db


def close_db(e=None):
    """
    If the connection exists, it is closed
    :param e:
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


# Python functions that will run the SQL commands found in the schema.sql file to the db.py file
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:  # opens a file relative to the flaskr package
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')  # defines a command called init-db that calls init_db function/shows success message
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    """
    Registered close_db and init_db_command with the application instance
    :param app:
    """
    app.teardown_appcontext(close_db)  # tells Flask to call the function when cleaning up after returning a response
    app.cli.add_command(init_db_command)  # adds a new command that can be called with the flask command
