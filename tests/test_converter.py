import random
import re

import pytest

from kroketalizer.converter import (_convert_names, _convert_string,
                                    _convert_to_kroket, _is_word,
                                    _replace_article_word, names)


@pytest.mark.parametrize("text, article_org, article_new, keyword, expected", [
    ('Het kroket bla', 'het', 'de', 'kroket', 'De kroket bla'),
    ('de nieuwe menu hier', 'de', 'het', 'menu', 'het nieuwe menu hier'),
    ('de nieuwe menu\'s hier', 'de', 'het', 'menu', 'de nieuwe menu\'s hier'),
])
def test_replace_article_word(text, article_org, article_new, keyword, expected):
    assert _replace_article_word(text, article_org, article_new, keyword) == expected


@pytest.mark.parametrize("text, ind_start, ind_end, expected", [
    ('hi there whats up', 0, 2, True),
    ('hi there whats up', 3, 8, True),
    ('hi there whats up', 4, 8, False),
    ('hi there whats up', 11, 15, False),
    ('hi there whats up', 15, 17, True),
])
def test_is_word(text, ind_start, ind_end, expected):
    assert _is_word(text, ind_start, ind_end) == expected


def _escape_names(text: str) -> str:
    return re.sub(rf"\b({'|'.join(re.escape(name) for name in names)})\b", '$$$', text)


@pytest.mark.parametrize("text, expected", [
    ('hi Het Concertgebouw', 'hi Het Kroketgebouw'),
    ('Grote Pianisten: Igor Levit speelt Schubert, Sjostakovitsj en Prokofjev',
     'Grote Frietbakkers: Igor $$$ bakt $$$, $$$ en $$$'),
    ('Kristiina Poska dirigeert Pärt en Sibelius', 'Kristiina $$$ frituurt $$$ en $$$'),
    (
        'Ook is er tijdelijk geen kaartverkoop (zowel online als offline) mogelijk.',
        'Ook is er tijdelijk geen bestelling (zowel binnen als buiten) mogelijk.',
     )
])
def test_convert_string(text, expected):
    converted = _escape_names(_convert_string(text))
    assert converted == expected


@pytest.mark.parametrize("text, expected", [
    ('hi Het Concertgebouw', 'hi Het Concertgebouw'),
    ('Over het gebouw', 'Over het gebouw'),
    ('Livestreams', 'Livestreams'),
    ('hi Marcel Something hier', 'hi Marcel $$$ hier'),
    ('Ferdinand Prokofiev Gerardus', 'Ferdinand $$$'),
    ('Dit hier. En dat.', 'Dit hier. En dat.'),
])
def test_convert_names(text, expected):
    converted = _escape_names(_convert_names(text))
    assert converted == expected


@pytest.mark.parametrize("text, expected", [
    ('hi Het Concertgebouw', 'hi Het Kroketgebouw'),
    ('Grote Pianisten:', 'Grote Frietbakkers:'),
])
def test_convert_to_kroket(text, expected):
    assert _convert_to_kroket(text) == expected

