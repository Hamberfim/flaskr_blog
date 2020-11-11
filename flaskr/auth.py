# -*- coding: utf-8 -*-
"""
Program: auth.py
Created on 11/11/2020
@author: adhamlin

This program creates the authentication blueprint. i.e., the authentication functions.
"""
# imports
import functools
# from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from flaskr.db import get_db

# the auth has views to register new users and to log in and log out
bp = Blueprint('auth', __name__, url_prefix='/auth')  # creates a Blueprint named 'auth'


# the /auth/register URL, (the register view) will return HTML with a form for a user to fill out.
@bp.route('/register', methods=('GET', 'POST'))  # associates the URL /register with the register view function
def register():
    """
    The register view
    :return: return HTML with a form for a user to fill out
    """
    if request.method == 'POST':  # a special type of dict mapping for submitted form keys/values
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        # validation that username and password are not empty,
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:  # that username is not already registered
            error = 'User {} is already registered.'.format(username)

        if error is None:  # if validation succeeds, insert the new user data into the database
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))  # used to securely hash the password in the db
            )
            db.commit()  # called to save the changes
            return redirect(url_for('auth.login'))  # generates the URL for login view, redirected to the login page

        flash(error)  # if validation fails, the error is shown to the user.

    return render_template('auth/register.html')


# follows the same pattern as the register view above
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)  # user is queried and stored in a var for later use
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):  # hashes the submitted password and compares them
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']  # stores data as cookie-flask signed data so that it can’t be tampered with
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


# a function that runs before the view function, no matter what URL is requested
@bp.before_app_request
def load_logged_in_user():
    """
    checks if a user id is stored in the session and gets that user’s data from the database, storing it on g.user
    """
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


# remove the user id from the session
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    """
    Checks if a user is loaded otherwise redirects to the login page.
    If a user is loaded the original view is called and continues normally
    url_for() generates the URL to a view based on name(endpoint) and arguments
    :param view:
    :return:
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))  # url_for() generates the URL to a view based on name and arguments

        return view(**kwargs)

    return wrapped_view
