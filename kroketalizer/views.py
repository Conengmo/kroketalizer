import os.path
import random
from flask import render_template
from scrapy.http import HtmlResponse

from . import app
from .cache import get_body_from_cache
from .converter import convert


@app.route("/")
def index():
    body = get_body_from_cache()
    r = HtmlResponse('', body=body)
    context = {
        'jumbotron_title': r.css('h1::text').get(),
        'jumbotron_text': r.css('h2::text').get(),
    }

    content = []
    images = [fn for fn in os.listdir('kroketalizer/static/img/') if fn.endswith('.jpg')]
    random.shuffle(images)
    for block in r.css('.infoblock'):
        header = block.css('.infoblock__content__header::text').get()
        texts = block.css('.usercontent > p::text').getall()
        if header and texts:
            content.append((header, texts, images.pop()))
    context['content'] = content

    context = convert(context)

    context['videos'] = [fn for fn in os.listdir('kroketalizer/static/video/') if fn.endswith('.mp4')]
    random.shuffle(context['videos'])

    return render_template('index.html', **context)


@app.route('/colofon')
def colofon():
    return render_template('colofon.html')