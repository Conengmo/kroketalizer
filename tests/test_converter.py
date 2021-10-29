import pytest

from kroketalizer.converter import _is_word, _replace_article_word


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
