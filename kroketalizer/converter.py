import re
from typing import Union


def convert(value: Union[str, dict, list, tuple]) -> Union[str, dict, list, tuple]:
    if isinstance(value, str):
        return _convert_string(value)
    elif isinstance(value, dict):
        return {_convert_string(key): convert(_value) for key, _value in value.items()}
    elif isinstance(value, list):
        return [convert(_value) for _value in value]
    elif isinstance(value, tuple):
        return tuple(convert(_value) for _value in value)
    else:
        raise ValueError(f'Unknown type: {type(value)}')


def _convert_string(text: str) -> str:
    text = _convert_to_kroket(text)
    text = _replace_article_words(text)
    return text


def _convert_to_kroket(text: str) -> str:
    text = re.sub(r'Concertgebouw', 'Kroketgebouw', text)
    text = re.sub(r'Concerten', 'Kroketten', text)
    text = re.sub(r'concerten', 'kroketten', text)
    text = re.sub(r'Concert', 'Kroket', text)
    text = re.sub(r'concert', 'kroket', text)
    return text


def _replace_article_words(text: str) -> str:
    """Replace wrong article words with correct versions."""
    article_org = 'het'
    len_article_org = 3
    article_new = 'de'
    keyword = 'kroket '
    len_keyword = 6  # kroket without the trailing space
    prev_ind = -1
    while True:
        b = text.lower()
        ind = b.find(keyword, prev_ind + 1)
        if ind == -1:
            break
        prev_ind = ind
        # Check if the word is not located in an html tag
        flg_skip = False
        for char in b[ind:ind - 300:-1]:
            if char == '>':
                break
            elif char == '<':
                flg_skip = True
        if flg_skip:
            continue
        ind_article = b.rfind(article_org, ind - 200, ind)
        if ind_article == -1:
            continue
        article_new_cap = article_new.capitalize() if text[ind_article].isupper() else article_new
        # fill = u'Replacing \'{}\' with \'{}{}\'.'
        # print(fill.format(text[ind_article:ind + len_keyword],
        #                   article_new_cap,
        #                   text[ind_article + len_article_org:ind + len_keyword]))
        text = text[:ind_article] + article_new_cap + text[ind_article + len_article_org:]
    return text
