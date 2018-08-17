import csv
import importlib
import os
import pkgutil

from datetime import datetime
from io import StringIO

from flask import Blueprint, Response


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
