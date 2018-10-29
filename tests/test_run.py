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
    if b'Kancolle Staff Twitter' in rv.data:
        pass
    else:
        exit(1)
