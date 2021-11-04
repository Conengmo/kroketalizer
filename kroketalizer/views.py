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

    images = [fn for fn in os.listdir('kroketalizer/static/img/') if fn.endswith('.jpg')]
    random.shuffle(images)

    content_top = []
    for block in r.css('.infoblock--current'):
        header = block.css('.infoblock__content__header::text').get()
        texts = block.css('.usercontent > p::text').getall()
        if header and texts:
            content_top.append((header, texts, images.pop()))
    context['content_top'] = content_top

    content_mid = []
    new_day = 0
    for block in r.css('.infoblock--highlight'):
        header = block.css('time::text').get()
        day_str = header.split()[0]
        new_day = max(new_day + 1, min(int(day_str) + random.randint(1, 6), 30))
        header = str(new_day) + header[len(day_str):]
        text = block.css('h2::text').get()
        if header and text:
            content_mid.append((header, text, images.pop()))
    context['content_mid'] = content_mid

    convert_bottom = []
    for block in r.css('.infoblock--experience'):
        header = block.css('.infoblock__content__header::text').get()
        texts = block.css('.usercontent > p::text').getall()
        if header and texts:
            convert_bottom.append((header, texts, images.pop()))
    context['content_bottom'] = convert_bottom

    context = convert(context)

    context['videos'] = [fn for fn in os.listdir('kroketalizer/static/video/') if fn.endswith('.mp4')]
    random.shuffle(context['videos'])

    return render_template('index.html', **context)


@app.route('/colofon')
def colofon():
    return render_template('colofon.html')