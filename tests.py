from os import access
import pytest
from db_accessor import DBAccessor
from init_db import init_db
from request_handler import RequestHandler
from datetime import date

accessor = init_db(None, True)
handler = RequestHandler(connection=accessor)

def test_create_artists():
    stones = "The Rolling Stones"
    handler.create_artist(stones)
    assert len(handler.get_artists()) == 1

    dylan = "Bob Dylan"
    handler.create_artist(dylan)
    assert len(handler.get_artists()) == 2

def test_get_artist_id():
    mccartney = "Paul McCartney"
    artist_id = handler.create_artist(mccartney)

    fetched_artist_id = handler.get_artist_id(mccartney)
    assert artist_id == fetched_artist_id

def test_create_albums():
    title = "Aftermath"
    release_date = date(1966, 4, 15)
    price = 5.0
    artist_name = "The Rolling Stones"

    row_id = handler.create_album(title, release_date, price, artist_name)
    assert row_id

    title = "Flowers"
    release_date = date(1967, 6, 26)
    price = 6.0
    artist_name = "The Rolling Stones"
    row_id = handler.create_album(title, release_date, price, artist_name)
    assert row_id

def test_create_album_invalid_artist():
    title = "Bogus"
    release_date = date(1995, 1, 1)
    price = 10.0
    artist_name = "Fake Artist"
    row_id = handler.create_album(title, release_date, price, artist_name)
    assert row_id is None

def test_get_albums():
    albums = handler.get_albums_for_artist("The Rolling Stones", False)
    assert len(albums) == 2

def test_add_tracks():
    album_title = "Aftermath"
    tracks = [("Paint It, Black", 3, 22), ("Under My Thumb", 3, 41)]
    handler.add_tracks(album_title, tracks)
    assert len(handler.get_tracks(album_title)) == len(tracks)

def test_add_tracks_fake_album():
    album_title = "Fake Album"
    tracks = [("Paint It, Black", 3, 22), ("Under My Thumb", 3, 41)]
    handler.add_tracks(album_title, tracks)
    assert len(handler.get_tracks(album_title)) == 0

def test_create_album_with_tracks():
    title = "The Rolling Stones"
    release_date = date(1964, 4, 16)
    price = 6.0
    artist_name = "The Rolling Stones"
    tracks = [("Route 66", 2, 20), ("Honest I Do", 2, 9), ("Carol", 2, 34)]
    row_id = handler.create_album(title, release_date, price, artist_name, tracks)
    assert row_id
    assert len(handler.get_tracks(title)) == len(tracks)

def test_get_albums_for_artist():
    assert len(handler.get_albums_for_artist("The Rolling Stones", True)) == 3
    assert len(handler.get_albums_for_artist("The Rolling Stones", True, filter_price=6)) == 2
    assert len(handler.get_albums_for_artist("The Rolling Stones", True, filter_price=5)) == 1