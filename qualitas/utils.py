import csv
import importlib
import os
import pkgutil

from datetime import datetime
from io import StringIO
from urllib.parse import urlparse, urljoin, quote

from flask import Blueprint, Response, request, url_for, redirect
from flask import Blueprint, Response
from inflection import parameterize
from werkzeug.routing import BaseConverter


def make_database_url():
    # Check for DATABASE_URL that is provided by heroku
    if 'DATABASE_URL' in os.environ and os.environ['DATABASE_URL']:
        return os.environ.get('DATABASE_URL')
    else:
        return 'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'.format(
            os.environ.get('DB_USER', 'postgres'),
            os.environ.get('DB_PASSWORD', ''),
            os.environ.get('DB_HOST', '127.0.0.1'),
            os.environ.get('DB_PORT', '5432'),
            os.environ.get('DB_NAME', 'tests'),
        )


def register_blueprints(app, package_name, package_path):
    """
    Register all Blueprint instances on the specified Flask application found
    in all modules for any found package

    :param app: the Flask application
    :param package_name: the package name
    :param package_path: the package path
    :return:
    """
    rv = []
    base_dir = package_path[0]
    for _, pkgname, ispkg in pkgutil.walk_packages([base_dir]):
        for _, modname, ismod in pkgutil.iter_modules(
                [os.path.join(base_dir, pkgname)]):
            m = importlib.import_module(
                '{0}.{1}.{2}'.format(package_name, pkgname, modname))
            for item in dir(m):
                item = getattr(m, item)
                if isinstance(item, Blueprint):
                    app.register_blueprint(item)
                rv.append(item)

    return rv


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
