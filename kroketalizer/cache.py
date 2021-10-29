import glob
import os
from datetime import date

import requests


def get_body_from_cache() -> bytes:
    url = 'https://www.concertgebouw.nl/'
    cache_filename = f'cache/{date.today()}.html'
    if not os.path.exists(cache_filename):
        for filename in glob.glob('cache/*'):
            os.remove(filename)
        resp = requests.get(url)
        resp.raise_for_status()
        with open(cache_filename, 'w') as f:
            f.write(resp.text)
        return resp.content
    else:
        with open(cache_filename, 'rb') as f:
            return f.read()
