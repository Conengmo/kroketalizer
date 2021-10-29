import random
import re
from string import ascii_lowercase
from typing import Union


def convert(value: Union[str, dict, list, tuple]) -> Union[str, dict, list, tuple]:
    if isinstance(value, str):
        return _convert_string(value)
    elif isinstance(value, dict):
        return {_convert_string(key): convert(_value) for key, _value in value.items()}
    elif isinstance(value, list):
        lst = [convert(_value) for _value in value]
        return [x for x in lst if x]
    elif isinstance(value, tuple):
        x = tuple(convert(_value) for _value in value)
        return x if all(x) else tuple()
    else:
        raise ValueError(f'Unknown type: {type(value)}')


def _convert_string(text: str) -> str:
    if text.endswith(('.jpg', '.mp4')):
        return text
    text = _skip_blocklist_entries(text)
    text = _convert_to_kroket(text)
    text = _replace_article_words(text)
    text = text.replace("'S", "'s")
    return text


conversions = {
    'concertgebouw': 'kroketgebouw',
    'concerten': 'kroketten',
    'concert': 'concert',
    'klinkt': 'smaakt',
    'mooier': 'beter',
    'dirigent': 'kok',
    'series': ['voordeelmenu\'s', 'combodeal\'s'],
    'programmering': 'menu',
    'philharmonisch orkest': ['filet americain', 'filodeeg bockworst', 'filet souflesse'],
    'vriendenloterij': 'gezinszak',
}


def _convert_to_kroket(text: str) -> str:
    for pattern, repl in conversions.items():
        if isinstance(repl, list):
            repl = random.sample(repl, 1)[0]
        text = _replace(pattern, repl, text)
    text = re.sub(rf'\bcorona', 'vogelgriep', text)
    return text


blocklist = [
    'condoleance',
]


def _skip_blocklist_entries(text: str) -> str:
    _text = text.lower()
    return '' if any(phrase in _text for phrase in blocklist) else text


def _replace(pattern, repl, text) -> str:
    for match in list(re.finditer(_re_phrase(pattern), text, re.I))[::-1]:
        is_capital = match[0][0].isupper()
        is_title = match[0].istitle()
        if is_title:
            repl = repl.title()
        elif is_capital:
            repl = repl.capitalize()
        span = match.span()
        text = text[:span[0]] + repl + text[span[1]:]
    return text


article_replacements = [
    ('het', 'de', 'kroket'),
    ('de', 'het', 'menu'),
]


def _replace_article_words(text: str) -> str:
    """Replace wrong article words with correct versions."""
    for article_org, article_new, keyword in article_replacements:
        text = _replace_article_word(text, article_org, article_new, keyword)
    return text


def _replace_article_word(text: str, article_org: str, article_new: str, keyword: str) -> str:
    len_article_org = len(article_org)
    for match in re.finditer(_re_phrase(keyword), text, re.I):
        ind = match.span()[0]
        match_article = re.search(_re_phrase(article_org[::-1]), text[ind - 200:ind][::-1], re.I)
        if not match_article:
            continue
        ind_article = ind - match_article.span()[1]
        article_new_cap = article_new.capitalize() if text[ind_article].isupper() else article_new
        text = text[:ind_article] + article_new_cap + text[ind_article + len_article_org:]
    return text


def _is_word(text: str, ind_start: int, ind_end: int):
    if ind_start > 0 and text[ind_start - 1] in ascii_lowercase:
        return False
    if ind_end < len(text) and text[ind_end] in ascii_lowercase:
        return False
    return True


def _re_phrase(phrase: str) -> str:
    return rf'\b{re.escape(phrase)}(?=([\s\t,._-])|$)'
