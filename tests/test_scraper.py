'''
Test module for vagalume_scraper app
'''

from vagalume_scraper.scraper import (
    _get_artist_page, _get_songs, _get_soup, _get_top_songs, _is_top,
    _get_all_songs_names
)
from vagalume_scraper.scraper import get_top_songs
from vagalume_scraper.scraper import get_song_lyrics
import pytest
import os

@pytest.mark.parametrize('artist, piece_of_html',
[
    ('ed-sheeran', '<title>Ed Sheeran - VAGALUME</title>'),
    ('shakira', '<title>Shakira - VAGALUME</title>'),
])
def test_get_artist_page_returns_html(artist, piece_of_html):
    assert piece_of_html in _get_artist_page(artist)

def test_get_artist_page_with_invalid_artist_returns_none():
    assert _get_artist_page('asdasdqwdas') is None

@pytest.fixture
def ed_soup():
    with open('./tests/ed.html', 'r') as html:
        return _get_soup(html.read())

@pytest.fixture
def joelma_soup():
    with open('./tests/joelma.html', 'r') as html:
        return _get_soup(html.read())

def test_get_songs(ed_soup, joelma_soup):
    assert ed_soup is not None
    assert joelma_songs is not None

    ed_song_divs = _get_songs(ed_soup)
    joelma_song_divs = _get_songs(joelma_soup)

    assert len(ed_song_divs) > 0
    assert len(joelma_song_divs) == 7

@pytest.fixture
def ed_songs():
    with open('./tests/ed.html', 'r') as html:
        return _get_songs(_get_soup(html.read()))

@pytest.fixture
def joelma_songs():
    with open('./tests/joelma.html', 'r') as html:
        return _get_songs(_get_soup(html.read()))

def test_song_is_top(ed_songs, joelma_songs):
    assert _is_top(ed_songs[0]) is True
    assert _is_top(ed_songs[-1]) is False
    for song in joelma_songs:
        assert _is_top(song) is False

@pytest.mark.parametrize('count',[
    17,
    20,
    25,
])
def test_get_top_songs(ed_songs, joelma_songs, count):
    ed_top_songs = _get_top_songs(ed_songs, count)
    joelma_top_songs = _get_top_songs(joelma_songs, count)

    assert len(ed_top_songs) == count
    assert ed_top_songs[1] == 'Perfect'
    assert ed_top_songs[10] == 'Give Me Love'
    assert ed_top_songs[17] == 'Kiss Me'
    
    # Empty dictionaries evaluate to False in Python
    assert bool(joelma_top_songs) is False

@pytest.mark.parametrize('artist, count, expected_songs, forbidden_songs', [
    ('ed-sheeran', 1, ['Perfect'], ['Photograph']),
    ('ed-sheeran', 12, ['Perfect', 'Addicted', 'Castle On The Hill'], ['Eraser', 'Don\'t']),
    ('eminem', 25, ['Kamikaze', 'Not Afraid'], [''])
])
def test_public_get_top_songs(artist, count, expected_songs, forbidden_songs):
    result = get_top_songs(artist, count)
    assert result['artist'] == artist
    for song in expected_songs:
        assert song in result['top_songs'].values()
    for song in forbidden_songs:
        assert song not in result['top_songs'].values()

def test_get_all_songs_names(ed_songs, joelma_songs):
    result_ed = _get_all_songs_names(ed_songs)
    result_joelma = _get_all_songs_names(joelma_songs)

    assert len(result_ed) == len(set(result_ed))
    assert 'Nina' in result_ed

    assert len(result_joelma) == 7
    assert 'Aqueles Tempos' in result_joelma

@pytest.mark.parametrize('first_letter', [
    'a',
    'A',
    'D',
    'g',
    'Z'
])
def test_get_all_songs_names_with_letter(ed_songs, joelma_songs, first_letter):
    result_ed = _get_all_songs_names(ed_songs, first_letter)
    result_joelma = _get_all_songs_names(joelma_songs, first_letter)

    assert len(result_ed) == len(set(result_ed))
    assert len(result_joelma) == len(set(result_joelma))

    for name in result_ed:
        assert (name.startswith(first_letter.upper())) or (name.startswith(first_letter))
    for name in result_joelma:
        assert (name.startswith(first_letter.upper())) or (name.startswith(first_letter))

def test_get_song_lyrics():
    lyrics = get_song_lyrics('ac-dc', 'jailbreak')

    assert bool(lyrics) is not False
    assert lyrics['artist'] == 'ac-dc'
    assert 'All in the name of liberty' in lyrics['lyrics']
