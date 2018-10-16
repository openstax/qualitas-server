from flask import Flask
from flask_security import SQLAlchemyUserDatastore

from .auth.models import User, Role
from .core import db, security
from .utils import register_blueprints
from .ext.markdown import Markdown, markdown
from .utils import register_blueprints, WikiTitleConverter, SlugConverter


def create_app(package_name, package_path, settings=None):
    """
    This function creates the application using the application factory pattern.
    Extensions and blueprints are then initialized onto the the application
    object.

    http://flask.pocoo.org/docs/0.11/patterns/appfactories/

    :param package_name: the name of the package
    :param package_path: the path of the package
    :param settings: override default settings via a python object
    :return: app: the main flask application object
    """

    app = Flask(package_name,
                instance_relative_config=True,
                template_folder='templates')

    app.config.from_pyfile('conf.py', silent=True)

    if settings:
        app.config.update(settings)

    db.init_app(app)
    app.security = security.init_app(app,
                                     SQLAlchemyUserDatastore(db, User, Role),
                                     register_blueprint=False)

    # register jinja2 extensions and filters
    jinja_extensions = [
        'jinja2.ext.do',
        'jinja2.ext.loopcontrols',
        'jinja2.ext.with_',
        Markdown
    ]

    app.jinja_options = app.jinja_options.copy()
    app.jinja_options['extensions'].extend(jinja_extensions)
    app.jinja_env.filters['markdown'] = markdown

    app.add_url_rule(
        '/favicon.ico', None, app.send_static_file,
        defaults={'filename': 'ico/rotary.ico'}
    )

    app.url_map.converters['wiki_title'] = WikiTitleConverter
    app.url_map.converters['slug'] = SlugConverter

    # Helper for auto-registering blueprints
    register_blueprints(app, package_name, package_path)

    return app
