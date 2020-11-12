# -*- coding: utf-8 -*-
"""
Program: blog.py
Created on 11/11/2020
@author: adhamlin

"""
# imports
from flask import (Blueprint, flash, g, redirect, render_template, request, url_for)
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    """
    # show all of the posts, with most recent first
    :return:
    """
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'  # JOIN used so the author info from user table is available
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
# login_required decorator you wrote in auth.py is used on the blog views so that a user must be logged in
# to visit these views, otherwise they will be redirected to the login page
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def get_post(id, check_author=True):
    """
    get the post and call it from each view,
    needed to fetch a post by id and check if the author matches the logged in user
    :param id:
    :param check_author:
    :return: return post by the id
    """
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))  # raise a exception that returns an HTTP status code

    # individual post where the user doesn't matter
    if check_author and post['author_id'] != g.user['id']:
        abort(403)  # # raise a exception that returns an HTTP status code

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
# login_required decorator you wrote in auth.py is used on the blog views so that a user must be logged in
# to visit these views, otherwise they will be redirected to the login page
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute('UPDATE post SET title = ?, body = ? WHERE id = ?', (title, body, id))
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))
