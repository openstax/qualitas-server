from flask import Flask
from flask_security import SQLAlchemyUserDatastore

from .auth.models import User, Role
from .auth.views import auth
from .core import (babel,
                   db,
                   github,
                   security,
                   zenhub)
from .dashboards.views import dashboards
from .ext.markdown import Markdown, markdown
from .home.views import home
from .tools.views import tools
from .utils import SlugConverter, WikiTitleConverter
from .wiki.views import wiki


def create_app(package_name, settings=None):
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

    # Attach extensions to main app
    babel.init_app(app)
    db.init_app(app)
    github.init_app(app)
    app.security = security.init_app(app,
                                     SQLAlchemyUserDatastore(db, User, Role),
                                     register_blueprint=False)
    zenhub.init_app(app)

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

    # Register blueprints
    app.register_blueprint(home, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(dashboards, url_prefix="/dashboards")
    app.register_blueprint(tools, url_prefix="/tools")
    app.register_blueprint(wiki, url_prefix="/wiki")

    return app
