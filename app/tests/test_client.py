import pytest

import sys
import os

container_folder = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..'
))
sys.path.insert(0, container_folder)

import my_pypi.app
from my_pypi.app import app as flask_app


@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    client = flask_app.test_client()

    try:
        my_pypi.app.register_blueprints()
    except Exception as x:
        # print(x)
        pass

    my_pypi.app.setup_db()

    yield client
