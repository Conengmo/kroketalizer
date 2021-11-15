import random
import re
from string import ascii_lowercase
from typing import List, Union


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
    text = _convert_names(text)
    text = _convert_to_kroket(text)
    text = _replace_article_words(text)
    text = text.replace("'S", "'s")
    text = re.sub(r'\s+', ' ', text)
    return text


names = [
    'Appelflap',
    'Berenklauw',
    'Frikandel',
    'Viandel',
    'Kroket',
    'Kwekkeboomkroket',
    'Goulashkroket',
    'Satekroket',
    'Garnalenkroket',
    'Groentenkroket',
    'Kaaskroket',
    'Kaasstengel',
    'Bamischijf',
    'Nasischijf',
    'Gehaktbal',
    'Gehaktstaaf',
    'Hete Donder',
    'Mexicano',
    'Ribster',
    'Zigeunerstick',
    'Vlampijp',
    'Kipkorn',
    'Kipcrush',
    'Grizly',
    'Sitostick',
    'Saterol',
    'Sate',
    'Shaslick',
    'Smulrol',
    'Shoarmarol',
    'Braadworst',
    'Ragoezie',
    'Loempia',
    'Visstick',
    'Viskroket',
    'Zeestick',
    'Loempidel',
    'Souflesse',
    'Taco',
    'Bonita',
    'Bitterbal',
    'Bittergarnituur',
    'Kipnugget',
    'Kipfinger',
    'Kipkrokantje',
    'Chickenwing',
    'Chickenstrip',
    'Truffelkroket',
    'Sparerib',
    'Halve-haan',
    'Schnitzel',
    'Shoarmarol',
    'Worstenbroodje',
    'Knackworst',
    'Bockworst',
    'Curry',
    'Joppiesaus',
    'Mosterd',
    'Appelmoes',
    'Fritessaus',
    'Puntbroodje',
    'Ketchup',
    'Piccalily',
    'Knoflooksaus',
    'Satesaus',
    'Mayonaise',
    'Milkshake',
    'Softijs',
    'Hamburger',
    'Vegaburger',
    'Remouladesaus',
    'Kibbeling',
    'Sundae',
    'Uitsmijter',
    'IJsstam',
]
names_lookup = {x[0]: x for x in names}


conversions_phrase = {
    'concertgebouw': 'kroketgebouw',
    'fonds': 'fooienpot',
    'klinkt': 'smaakt',
    'mooier': 'beter',
    'dirigent': 'kok',
    'series': ['voordeelmenu\'s', 'combodeal\'s'],
    'programmering': 'menu',
    'philharmonisch': ['filet americain', 'filodeeg'],
    'orkest': '',
    'vriendenloterij': 'gezinszak',
    'dirigeert': 'frituurt',
    'pianisten': 'frietbakkers',
    'speelt': 'bakt',
    'kassa': 'fruitautomaat',
    'kaartverkoop': 'bestelling',
    'kaartverkoopsysteem': 'bestelsysteem',
    'online': 'binnen',
    'offline': 'buiten',
    'kaarten': 'friet',
    'schermen': 'toonbank',
    'evenement': 'partijtje',
    'concert of evenement': 'kinderpartijtje',
    'Collegium Vocale Gent': 'collegium friture',
}


conversions_partial = {
    'concerten': 'kroketten',
    'concert': 'kroket',
    'corona': 'vogelgriep',
}


def _convert_names(text: str) -> str:
    new_sentences = []
    for sentence in text.split('. '):
        name_parts = []
        new_text_parts = []
        for i, word in enumerate(sentence.split()):
            word_lower = word.lower().rstrip(',:')
            if word.istitle() and (word_lower in conversions_phrase or any(x in word_lower for x in conversions_partial)):
                new_text_parts.extend(name_parts)
                name_parts = []
                new_text_parts.append(word)
                continue
            if word.istitle():
                name_parts.append(word)
            elif name_parts and i == 1:
                new_text_parts.extend(name_parts)
                name_parts = []
                new_text_parts.append(word)
            elif name_parts and i > 1:
                new_text_parts.append(_convert_names_sub(name_parts))
                name_parts = []
                new_text_parts.append(word)
            else:
                new_text_parts.append(word)
            if name_parts and word.endswith((':', ',', '.')):
                new_text_parts.append(_convert_names_sub(name_parts) + word[-1])
                name_parts = []
        if name_parts and i > 0:
            new_text_parts.append(_convert_names_sub(name_parts))
        else:
            new_text_parts.extend(name_parts)
        new_sentences.append(' '.join(new_text_parts))
    return '. '.join(new_sentences)


def _convert_names_sub(name_parts: List[str]) -> str:
    if len(name_parts) == 1:
        return random.sample(names, 1)[0]
    else:
        return name_parts[0] + ' ' + (names_lookup.get(name_parts[0][0]) or random.sample(names, 1)[0])


def _convert_to_kroket(text: str) -> str:
    for pattern, repl in sorted(conversions_phrase.items(), key=lambda x: len(x[0]), reverse=True):
        if isinstance(repl, list):
            repl = random.sample(repl, 1)[0]
        text = _replace(_re_phrase(pattern), repl, text)
    for pattern, repl in conversions_partial.items():
        text = _replace(re.escape(pattern), repl, text)
    return text


blocklist = [
    'condoleance',
]


def _skip_blocklist_entries(text: str) -> str:
    _text = text.lower()
    return '' if any(phrase in _text for phrase in blocklist) else text


def _replace(pattern: str, repl: str, text: str) -> str:
    for match in list(re.finditer(pattern, text, re.I))[::-1]:
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
    return rf'\b{re.escape(phrase)}(?=([\s\t\):,._-])|$)'
