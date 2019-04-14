import os

from qualitas.utils import make_database_url


def test_make_database_url():
    test_url = 'postgresql+psycopg2://postgres:@127.0.0.1:5433/testdb'
    url_template = 'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'
    test_db_name = 'pizza'
    test_db_port = '2222'
    test_db_user = 'leonardo'
    test_db_host = '0.0.0.0'
    test_db_password = 'cowabunga'

    os.environ['DATABASE_URL'] = test_url
    url = make_database_url()
    assert url == test_url
    assert test_db_name not in url
    assert test_db_port not in url
    assert test_db_user not in url

    os.environ['DATABASE_URL'] = ""
    os.environ['DB_NAME'] = test_db_name
    os.environ['DB_HOST'] = test_db_host
    os.environ['DB_USER'] = test_db_user
    os.environ['DB_PORT'] = test_db_port
    os.environ['DB_PASSWORD'] = test_db_password

    # Test default
    url = make_database_url()

    assert url == url_template.format(test_db_user,
                                      test_db_password,
                                      test_db_host,
                                      test_db_port,
                                      test_db_name)


