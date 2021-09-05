from flask import Blueprint
from flask import request
from flask import abort
from flask import jsonify
from vagalume_scraper.scraper import get_top_songs
from vagalume_scraper.scraper import get_all_songs_names
from vagalume_scraper.scraper import get_song_lyrics

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/<artist>')
def top_songs(artist, methods=('GET',)):
    '''
    Returns top 15 songs from <artist> in JSON format.

    Optional <count> URL parameter for more
    or less songs (minimum 0, max 25)
    '''
    count = request.args.get('count', default=15, type=int)
    if count > 25 or count < 0:
        response = abort(400)
    else:
        payload = get_top_songs(artist, count)
        # empty dicts are evaluated as False
        if bool(payload) is False:
            response = ('Artist not found', 204)
        elif bool(payload['top_songs']) is False:
            response = ('No top songs for artist', 204)
        else:
            response = jsonify(get_top_songs(artist, count))
    return response

@bp.route('/<artist>/all')
def all_songs(artist, methods=('GET',)):
    '''
    Returns all songs from <artist> in JSON format.
    '''
    payload = get_all_songs_names(artist)
    if bool(payload) is False:
        response = ('Artist not found', 204)
    else:
        response = jsonify(payload)
    return response

@bp.route('/<artist>/<letter>')
def songs_start_with_letter(artist, letter, methods=('GET',)):
    '''
    Return all songs from <artist> with a title starting with <letter>
    in JSON format.
    '''
    if len(letter) > 1:
        return abort(400)

    payload = get_all_songs_names(artist, first_letter=letter)
    if bool(payload) is False:
        response = ('Artist not found', 204)
    elif bool(payload) is not False and bool(payload['songs']) is False:
        response = ('No songs found with letter', 204)
    else:
        response = jsonify(payload)
    return response

@bp.route('/<artist>/lyrics/<title>')
def song_lyrics(artist, title, methods=('GET',)):
    '''
    Returns the lyrics for song with <title> played by <artist> in JSON format
    '''
    if len(title) < 1:
        return abort(400)
    
    payload = get_song_lyrics(artist, title)
    if bool(payload) is False:
        response = ('Artist not found', 204)
    elif bool(payload['lyrics']) is False:
        response = ('Lyrics nto found', 204)
    else:
        response = jsonify(payload)
    return response