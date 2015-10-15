from url_shortener import app
import sqlite3
from flask import request
from flask import g
from flask import render_template
from flask import redirect
import base64
import struct
import random
import sys


def get_id():
    n = random.randint(0, sys.maxint)
    s = struct.pack(">Q", n)
    return base64.urlsafe_b64encode(s)[:-1]  # strip trailing =


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_db()
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.errorhandler(404)
def not_found():
    return 'not found', 404


@app.route("/<short_url>")
def redir_short_url(short_url):
    db = get_db()
    row = query_db('select * from links where short = ?', (short_url,), one=True)
    if row is None:
        return not_found()
    return redirect(row['long'])


@app.route("/")
def hello():
    db = get_db()
    return "Hello World!"


@app.route("/links", methods=['POST'])
def new_link():
    url = request.form.get('url', None)
    if url is None:
        return 'Why'
    db = get_db()
    short_url = get_id()
    db.cursor().execute("insert into links(short, long) values (?, ?)", (short_url, url))
    db.commit()
    return short_url
