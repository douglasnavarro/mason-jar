'''
This module provides functions to extract data from www.vagalume.com.br
'''

import requests
from bs4 import BeautifulSoup

def _get_artist_page(artist):
    '''
    Fetches html page for artist
    e.g https://www.vagalume.com.br/<artist>/
    '''
    response = requests.get('https://www.vagalume.com.br/{}/'.format(artist))
    if response.status_code == 200:
        response.encoding = 'utf-8'
        return response.text
    else:
        return None

def _get_lyrics_page(artist, title):
    '''
    Fetches html page for song
    e.g https://www.vagalume.com.br/<artist>/<title>.html
    '''
    response = requests.get('https://www.vagalume.com.br/{}/{}.html'.format(artist, title))
    if response.status_code == 200:
        response.encoding = 'utf-8'
        return response.text
    else:
        return None

def _get_lyrics(soup):
    lyrics = soup.find('div', id='lyrics')
    for br in lyrics.find_all('br'):
        br.replace_with('\n')
    return lyrics.text

def _get_soup(page_html):
    '''
    Returns bs4.BeautifulSoup object generated from html page
    '''
    return BeautifulSoup(page_html, 'html.parser')

def _get_songs(page_soup):
    '''
    Returns all songs from one artist page
    The return value is a bs4.element.ResultSet object,
    which is also a list (empty if no songs were found)
    '''
    return page_soup.find_all(class_='flexSpcBet')

def _is_top(song):
    '''
    Returns True if song is ranked in artist TOP list
    '''
    # Only top songs divs have a 'span' tag class="numMusic" inside
    return song.find('span', class_='numMusic') is not None

def _get_top_songs(songs, count):
    '''
    Returns dictionary of top songs with items
    position: song title
    from indexes 0 to count

    If the artist has no top songs, returns empty dict
    '''
    top_songs = {}
    for song in songs[0:count]:
        if _is_top(song):
            title = song.find('a', class_='nameMusic').text
            number = song.find('span', class_='numMusic').text
            number = int(number[:-1])
            top_songs[number] = title
    return top_songs

def get_top_songs(artist, count):
    '''
    Public function to return top songs from artist
    '''
    result = {}
    page = _get_artist_page(artist)
    if page is not None:
        soup = _get_soup(page)
        songs = _get_songs(soup)
        top_songs = _get_top_songs(songs, count)
        result = {'artist': artist, 'top_songs': top_songs}
    return result

def _get_all_songs_names(songs, first_letter=None):
    '''
    Receives a list all songs (top included) from _get_songs
    and returns a list of song names with no duplicates
    '''
    top_removed =  [song for song in songs if _is_top(song) is False]
    song_names = [song.find('a', class_="nameMusic").text for song in top_removed]
    if first_letter is not None:
        song_names = [
            song for song in song_names if song.startswith(first_letter.upper())
            ]
    return song_names

def get_all_songs_names(artist, first_letter=None):
    '''
    Public function to return all songs names from artist
    '''
    result = {}
    page = _get_artist_page(artist)
    if page is not None:
        soup = _get_soup(page)
        songs = _get_songs(soup)
        names = _get_all_songs_names(songs, first_letter)
        result = {'artist': artist, 'songs': names}
    return result

def get_song_lyrics(artist, title):
    '''
    Gets song lyrics 
    '''
    result = {}
    page = _get_lyrics_page(artist, title)
    if page is not None:
        soup = _get_soup(page)
        lyrics = _get_lyrics(soup)
        result = {
            'artist': artist,
            'title': title,
            'lyrics': lyrics
        }
    return result