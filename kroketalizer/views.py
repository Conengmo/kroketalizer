import os.path
import random

from flask import render_template

from . import app
from .cache import get_body_from_cache
from .converter import convert
from .scrape import get_content


@app.route("/")
def index():
    body = get_body_from_cache()

    context = get_content(body)

    context = convert(context)

    context['videos'] = [fn for fn in os.listdir('kroketalizer/static/video/') if fn.endswith('.mp4')]
    random.shuffle(context['videos'])

    return render_template('index.html', **context)


@app.route('/colofon')
def colofon():
    return render_template('colofon.html')