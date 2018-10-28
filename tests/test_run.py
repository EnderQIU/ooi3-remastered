import pytest

from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        app.run()

    yield client
