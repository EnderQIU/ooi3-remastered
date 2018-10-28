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
    """Start with a blank database."""

    rv = client.get('/')
    if b'OOI' in rv.data:
        pass
    else:
        exit(1)
