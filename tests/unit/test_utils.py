import os

import pytest

from qualitas.utils import make_database_url

URL_TEMPLATE = 'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'


@pytest.mark.parametrize('url_template,db_user,db_password,db_host,db_port,db_name',
                         [(URL_TEMPLATE, 'leonardo', 'cowabunga', '127.0.0.1', '5432', 'pizza_db')])
def test_make_database_url_heroku(url_template, db_user, db_password, db_host, db_port, db_name):
    test_url = url_template.format(db_user, db_password, db_host, db_port, db_name)

    os.environ['DATABASE_URL'] = test_url
    os.environ['DB_USER'] = 'test_user'
    os.environ['DB_PASSWORD'] = 'test_password'
    os.environ['DB_HOST'] = 'test_host'
    os.environ['DB_PORT'] = 'test_port'
    os.environ['DB_NAME'] = 'test_name'

    url = make_database_url()

    assert url == test_url


@pytest.mark.parametrize('url_template,db_user,db_password,db_host,db_port,db_name',
                         [(URL_TEMPLATE, 'postgres', '', 'db', '5432', 'tests')])
def test_make_database_url_with_env_vars(url_template, db_user, db_password, db_host, db_port,
                                         db_name):
    os.environ['DATABASE_URL'] = ''
    os.environ['DB_USER'] = db_user
    os.environ['DB_PASSWORD'] = db_password
    os.environ['DB_HOST'] = db_host
    os.environ['DB_PORT'] = db_port
    os.environ['DB_NAME'] = db_name

    test_url = url_template.format(db_user, db_password, db_host, db_port, db_name)

    url = make_database_url()

    assert url == test_url


@pytest.mark.parametrize('url_template,db_user,db_host,db_port,db_name',
                         [(URL_TEMPLATE, 'postgres', 'db', '5432', 'tests')])
def test_make_database_url_raise_environment_error(url_template, db_user, db_host, db_port,
                                                   db_name):
    os.environ['DATABASE_URL'] = ''
    del os.environ['DB_PASSWORD']
    os.environ['DB_USER'] = db_user
    os.environ['DB_HOST'] = db_host
    os.environ['DB_PORT'] = db_port
    os.environ['DB_NAME'] = db_name

    with pytest.raises(EnvironmentError):
        assert make_database_url()
