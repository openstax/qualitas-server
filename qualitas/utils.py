import csv
import os

from datetime import datetime
from io import StringIO
from urllib.parse import urlparse, urljoin, quote

from flask import (redirect,
                   Response,
                   request,
                   url_for)
from inflection import parameterize
from werkzeug.routing import BaseConverter


def make_database_url(**environ):
    """Creates a database_url based on defaults or environment variables.

    Heroku provides access to the database via a `DATABASE_URL` environment
    variable. This function's main purpose is to check if this is provided and
    if not to make a database url based on default values or environment
    variables.

    :param environ: a dictionary of values used to create a database url
    :type environ: dict
    :return: a string representation of a database url
    """
    mandatory_vars = ['DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT', 'DB_NAME']
    if not environ:
        environ = os.environ
    # Check for DATABASE_URL that is provided by heroku
    if 'DATABASE_URL' in environ and environ['DATABASE_URL']:
        return environ.get('DATABASE_URL')
    else:
        for var in mandatory_vars:
            if var not in environ:
                raise EnvironmentError("Failed because {} is not set.".format(var))
        return 'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'.format(
            environ['DB_USER'],
            environ['DB_PASSWORD'],
            environ['DB_HOST'],
            environ['DB_PORT'],
            environ['DB_NAME'],
        )


# http://flask.pocoo.org/snippets/62/
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))

    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def get_redirect_target():
    for target in request.form.get('next'), request.args.get('next'), request.referrer:
        if not target:
            continue

        if is_safe_url(target):
            return target


def redirect_next(endpoint='home.index', **values):
    target = get_redirect_target()

    if not target:
        target = url_for(endpoint, **values)

    return redirect(target)


def to_csv(fieldnames, collection):

    def make_writer(sio, fieldnames):
        return csv.DictWriter(sio, fieldnames, dialect='excel')

    sio = StringIO()
    w = make_writer(sio, fieldnames=fieldnames)
    w.writeheader()
    yield sio.getvalue()

    for row in collection:
        sio = StringIO()
        w = make_writer(sio, fieldnames=fieldnames)
        w.writerow(row)
        yield sio.getvalue()


def render_csv(fieldnames, collection, filename, datestamp=True):
    if datestamp:
        filename = datetime.now().strftime(filename + '-%Y%m%d.csv')
    else:
        filename = filename + '.csv'

    return Response(to_csv(fieldnames, collection),
                    mimetype='text/csv',
                    headers={'Content-Disposition':
                             'attachment;filename={}'.format(filename)})


class WikiTitleConverter(BaseConverter):
    """Matches words separated by spaces or underscores.

    When parsing the url, underscores are converted to spaces.
    When building the url, spaces are converted to underscores.
    """

    def to_python(self, value):
        return value.replace('_', ' ')

    def to_url(self, value):
        return quote(value.replace(' ', '_'))


class SlugConverter(BaseConverter):
    """Matches an int id and optional slug, separated by "/".

    :param attr: name of field to slugify, or None for default of str(instance)
    :param length: max length of slug when building url
    """

    regex = r'-?\d+(?:/[\w\-]*)?'

    def __init__(self, map, attr=None, length=80):
        self.attr = attr
        self.length = int(length)

        super(SlugConverter, self).__init__(map)

    def to_python(self, value):
        id, slug = (value.split('/') + [None])[:2]

        return int(id)

    def to_url(self, value):
        raw = str(value) if self.attr is None else getattr(value, self.attr, '')
        slug = parameterize(raw)[:self.length].rstrip('-')

        return '{}/{}'.format(value.id, slug).rstrip('/')
