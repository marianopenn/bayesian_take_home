from os import access
import pytest
from db_accessor import DBAccessor
from init_db import init_db
from request_handler import RequestHandler

accessor = init_db(None, True)
handler = RequestHandler(connection=accessor)

def test_create_artists():
    stones = "The Rolling Stones"
    handler.create_artist(stones)
    assert len(handler.get_artists()) == 1

    dylan = "Bob Dylan"
    handler.create_artist(dylan)
    assert len(handler.get_artists()) == 2

