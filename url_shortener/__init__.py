from flask import Flask

DATABASE = '/tmp/url-short-db'

app = Flask(__name__)
app.config.from_object(__name__)

import url_shortener.views
