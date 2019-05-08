import os
import uuid

from qualitas.utils import make_database_url


# SETTINGS

# MAIN FLASK APPLICATION
DEBUG = os.environ.get('FLASK_DEBUG', False)
SECRET_KEY = os.environ.get('SESSION_SECRET', str(uuid.uuid4()))
SQLALCHEMY_DATABASE_URI = make_database_url(db_name="qualitas_db")
SQLALCHEMY_TRACK_MODIFICATIONS = False
SERVER_NAME = os.environ.get('FLASK_SERVER_NAME', None)
PREFERRED_URL_SCHEME = os.environ.get('FLASK_PREFERRED_URL_SCHEME', 'http')

# GITHUB
GITHUB_USER = os.environ.get('GITHUB_USER', None)
GITHUB_PASSWORD = os.environ.get('GITHUB_PASSWORD', None)
GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID', None)
GITHUB_CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET', None)
GITHUB_AUTH_ENABLED = os.environ.get('GITHUB_AUTH_ENABLED', True)
GITHUB_AUTH_TOKEN = os.environ.get('GITHUB_AUTH_TOKEN', None)

# ZENHUB
ZENHUB_TOKEN = os.environ.get('ZENHUB_TOKEN')

# Flask-Security
SECURITY_CONFIRMABLE = False
SECURITY_REGISTERABLE = False
SECURITY_RECOVERABLE = False
SECURITY_TRACKABLE = True
SECURITY_CHANGEABLE = False
SECURITY_BLUEPRINT_NAME = 'auth'

# Flask-Babel
BABEL_DEFAULT_TIMEZONE = os.environ.get('BABEL_DEFAULT_TIMEZONE', 'America/Chicago')
