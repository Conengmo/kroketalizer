import os
import random

from scrapy.http import HtmlResponse


def get_content(body: bytes) -> dict:
    r = HtmlResponse('', body=body)
    context = {}
    images = [fn for fn in os.listdir('kroketalizer/static/img_random/') if fn.endswith('.jpg')]
    random.shuffle(images)

    content_top = []
    seen_header = set()
    for block in r.css('article[data-v-07ebc5fe=""]'):
        header = block.css('h3::text').get().strip()
        text = block.css('span::text').get().strip()
        if header and text and header not in seen_header:
            content_top.append((header, text, images.pop()))
            seen_header.add(header)
        if len(content_top) == 2:
            break
    context['content_top'] = content_top

    content_mid = []
    new_day = 0
    for block in r.css('article[data-component="CardEventCompact"]'):
        header = block.css('time::text').get().strip()
        header = header[3:]  # remove day
        day_str = header.split()[0]
        new_day = max(new_day + 1, min(int(day_str) + random.randint(1, 6), 30))
        header = str(new_day) + header[len(day_str):]
        text = block.css('h3::text').get().strip()
        if header and text:
            content_mid.append((header, text, images.pop()))
        if len(content_mid) == 3:
            break
    context['content_mid'] = content_mid

    convert_bottom = []
    for block in r.css('a[data-component="Cardoverview"]'):
        header = block.css('h4::text').get().strip()
        texts = block.css('h5::text').get().strip()
        if 'restaurant' in header.lower() or 'café' in header.lower():
            continue
        if header and texts:
            convert_bottom.append((header, texts, images.pop()))
    context['content_bottom'] = convert_bottom

    return context
