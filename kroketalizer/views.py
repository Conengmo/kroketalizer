import os.path
import random

import requests
from flask import render_template
from scrapy.http import HtmlResponse

from . import app
from .converter import convert


@app.route("/")
def index():
    url = 'https://www.concertgebouw.nl/'
    if not os.path.exists('dump.html'):
        resp = requests.get(url)
        resp.raise_for_status()
        with open('dump.html', 'w') as f:
            f.write(resp.text)
        body: bytes = resp.content
    else:
        with open('dump.html', 'rb') as f:
            body = f.read()
    r = HtmlResponse(url, body=body)
    context = {
        'jumbotron_title': r.css('h1::text').get(),
        'jumbotron_text': r.css('h2::text').get(),
    }

    content = []
    images = os.listdir('kroketalizer/static/img/')
    random.shuffle(images)
    for block in r.css('.infoblock'):
        header = block.css('.infoblock__content__header::text').get()
        texts = block.css('.usercontent > p::text').getall()
        if header and texts:
            content.append((header, texts, images.pop()))
    context['content'] = content

    context = convert(context)

    context['videos'] = os.listdir('kroketalizer/static/video/')
    random.shuffle(context['videos'])

    return render_template('index.html', **context)
