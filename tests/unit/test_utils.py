import os

import pytest

from qualitas.utils import make_database_url

URL_TEMPLATE = 'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'


@pytest.mark.parametrize('url_template,db_name,db_user,db_password,db_host,db_port',
                         [(URL_TEMPLATE, 'pizza', 'leonardo', 'cowabunga', '127.0.0.1', 5432)])
def test_make_database_url_heroku(url_template, db_name, db_user, db_password, db_host, db_port):
    test_url = url_template.format(db_user, db_password, db_host, db_port, db_name)

    url = make_database_url()
    assert not (url == test_url)

    os.environ['DATABASE_URL'] = test_url
    url = make_database_url()

    assert url == test_url


@pytest.mark.parametrize('url_template,db_name,db_user,db_password,db_host,db_port',
                         [(URL_TEMPLATE, 'tests', 'postgres', '', 'db', 5432)])
def test_make_database_url_default(url_template, db_name, db_user, db_password, db_host, db_port):

    os.environ['DATABASE_URL'] = ''

    test_url = url_template.format(db_user, db_password, db_host, db_port, db_name)

    url = make_database_url()

    assert url == test_url


