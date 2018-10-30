import os

import pytest

from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = os.urandom(24)
    client = app.test_client()

    yield client


def test_index(client):
    """
    Test the index page whether loaded normally
    :param client:
    """

    rv = client.get('/')
    assert b'Kancolle Staff Twitter' in rv.data, 'index test failed'


def test_twitter(client):
    """
    Test the twitter api
    :param client:
    :return:
    """
    rv = client.get('/ooiapi/twitter')
    assert b'ok' in rv.data, 'twitter api test failed'
