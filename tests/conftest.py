import os

import pytest
from webtest import TestApp

from qualitas import create_app


credentials = [
    os.environ.get("GITHUB_USER", "foo"),
    os.environ.get("GITHUB_PASSWORD", "bar"),
    os.environ.get("GITHUB_AUTH_TOKEN", None)
]


@pytest.fixture(scope='session')
def app_config():
    """The config for the test application"""
    settings = {
        'TESTING': True,
        'SECRET_KEY': 'a key for testing',
        'DEBUG': True,
        'GITHUB_USER': credentials[0],
        'GITHUB_PASSWORD': credentials[1],
        'GITHUB_AUTH_TOKEN': credentials[2]
    }

    return settings


@pytest.fixture(scope='session')
def app(app_config):
    """The test application"""
    _app = create_app()
    _app.config.update(app_config)

    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope='function')
def test_client(app):
    """
    Configure a WebTest client for nice convenience methods."""
    return TestApp(app)
