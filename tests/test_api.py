'''
Test module for vagalume_api flask app

This script gathers both unit tests and
test setups as the app is relatively simple
'''

import pytest
import json
from vagalume_api import create_app

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
    })

    yield app

@pytest.fixture
def client(app):
    return app.test_client()

# basic tests
def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Mason Jar API' in response.data

# api tests
@pytest.mark.parametrize('artist',
[
    'ed-sheeran',
    'shakira',
])
def test_top_songs_default(client, artist):
    response = client.get('/api/{}'.format(artist))
    json_data = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert json_data['artist'] == artist
    assert len(json_data['top_songs']) == 15
    assert '' not in json_data['top_songs']


@pytest.mark.parametrize('artist, songs, forbidden_songs, count',
[
    ('ed-sheeran', ['Perfect', 'Photograph', 'Shape Of You'], ['Perfect Symphony (With Andrea Bocelli)'], 3),
    ('shakira', ['Loca', 'Inevitable'], ['1968'], 20),
])
def test_top_songs_with_count(client, artist, songs, forbidden_songs, count):
    response = client.get('/api/{}?count={}'.format(artist, count))
    if int(count) > 25:
        assert response.status_code == 400, 'count parameter over 25 must get bad request!'
    else:
        assert response.status_code == 200
        assert artist in response.data.decode('utf-8')
        for song in songs:
            assert song in response.data.decode('utf-8')
        for song in forbidden_songs:
            assert song not in response.data.decode('utf-8')

@pytest.mark.parametrize('artist, expected_songs', [
    ('ed-sheeran', ['Photograph', 'Perfect', 'Sara']),
    ('joelma', ['Aqueles Tempos', 'Pode Entrar'])
])
def test_all_songs(client, artist, expected_songs):
    response = client.get('/api/{}/all'.format(artist))
    assert response.status_code == 200

    data = json.loads(response.data.decode('utf-8'))
    
    assert data['artist'] == artist
    assert len(data['songs']) == len(set(data['songs']))
    for song in expected_songs:
        assert song in data['songs']

@pytest.mark.parametrize('artist, letter, expected_songs, forbidden_songs', [
    ('ed-sheeran', 'a', ['Autumn Leaves', 'Afire Love'], ['Dive', '...Baby One More time']),
    ('iron-maiden', 'D', ['Deja Vu', 'Dance Of Death'], ['Fear of The Dark'])
])
def test_songs_with_letter(client, artist, letter, expected_songs, forbidden_songs):
    response = client.get('/api/{}/{}'.format(artist, letter))
    assert response.status_code == 200

    data = json.loads(response.data.decode('utf-8'))

    assert data['artist'] == artist
    assert len(data['songs']) == len(set(data['songs']))
    for song in expected_songs:
        assert song in expected_songs
        assert song not in forbidden_songs