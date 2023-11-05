import os.path
import random

from flask import render_template

from . import app
from .cache import get_body_from_cache
from .converter import convert, names
from .scrape import get_content


@app.route("/")
def index():
    body = get_body_from_cache()

    context = get_content(body)

    context = convert(context)

    return render_template('index.html', **context)


@app.route('/colofon')
def colofon():
    return render_template('colofon.html')