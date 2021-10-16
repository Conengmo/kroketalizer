import requests
from flask import render_template
from scrapy.http import HtmlResponse

from . import app
from .converter import convert


@app.route("/")
def index():
    resp = requests.get('https://www.concertgebouw.nl/')
    resp.raise_for_status()
    r = HtmlResponse(resp.url, body=resp.content)
    context = {
        'jumbotron_title': r.css('h1::text').get(),
        'jumbotron_text': r.css('h2::text').get(),
    }

    content = []
    for block in r.css('.infoblock'):
        header = block.css('.infoblock__content__header::text').get()
        texts = block.css('.usercontent > p::text').getall()
        if header and texts:
            content.append((header, texts))
    context['content'] = content

    context = convert(context)

    return render_template('index.html', **context)
