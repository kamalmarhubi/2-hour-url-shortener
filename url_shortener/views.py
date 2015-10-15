from url_shortener import app
import sqlite3
from flask import request
from flask import g
from flask import render_template


def connect_db():
        return sqlite3.connect(app.config['DATABASE'])


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


@app.route("/")
def hello():
    db = get_db()
    return "Hello World!"


@app.route("/links", methods=['POST'])
def new_link():
    return str(request.form)
