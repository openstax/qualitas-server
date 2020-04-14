import os

import pytest
from alembic.command import upgrade
from alembic.config import Config as AlembicConfig

from pytest_postgresql.factories import (init_postgresql_database,
                                         drop_postgresql_database)
from webtest import TestApp

from qualitas import create_app


credentials = [
    os.environ.get("GITHUB_USER", "foo"),
    os.environ.get("GITHUB_PASSWORD", "bar"),
    os.environ.get("ZENHUB_TOKEN", "x" * 20)
]


@pytest.fixture(scope='function', autouse=True)
def set_database_name(monkeypatch):
    monkeypatch.setenv("DB_NAME", "tests")


@pytest.fixture(scope='session')
def config_database(request):
    connection_template = 'postgresql+psycopg2://{0}@{1}:{2}/{3}'

    pg_host = os.environ.get('DB_HOST', 'db')
    pg_port = os.environ.get('DB_PORT', 5432)
    pg_user = os.environ.get('DB_USER', 'postgres')
    pg_db = 'tests'
    connection_string = connection_template.format(pg_user,
                                                   pg_host,
                                                   pg_port,
                                                   pg_db)

    # Create the database
    init_postgresql_database(pg_user, pg_host, pg_port, pg_db)

    yield connection_string

    # Ensure the database gets deleted
    drop_postgresql_database(
        pg_user, pg_host, pg_port, pg_db, '11'
    )


@pytest.fixture(scope='session')
def app_config(config_database):
    """The config for the test application"""
    settings = {
        'TESTING': True,
        'SECRET_KEY': 'a key for testing',
        'DEBUG': True,
        'SQLALCHEMY_DATABASE_URI': config_database,
        'WTF_CSRF_ENABLED': False,
        'GITHUB_USER': credentials[0],
        'GITHUB_PASSWORD': credentials[1],
        'ZENHUB_TOKEN': credentials[2]
    }

    # Run Database migrations
    config = AlembicConfig('alembic.ini')
    config.set_main_option('sqlalchemy.url', config_database)
    print('\n----- RUN ALEMBIC MIGRATION -----\n')
    upgrade(config, 'head')

    return settings


@pytest.fixture(scope='session')
def app(app_config):
    """The test application"""
    _app = create_app()
    _app.config.update(app_config)

    ctx = _app.test_request_context()
    ctx.push()

    yield _app


@pytest.fixture(scope='function')
def test_client(app):
    """
    Configure a WebTest client for nice convenience methods."""
    return TestApp(app)
