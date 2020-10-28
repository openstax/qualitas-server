import os
import uuid

from qualitas.utils import make_database_url

# SETTINGS

# MAIN FLASK APPLICATION
DEBUG = os.environ.get('FLASK_DEBUG', False)
SECRET_KEY = os.environ.get('SESSION_SECRET', str(uuid.uuid4()))
SERVER_NAME = os.environ.get('FLASK_SERVER_NAME', None)
PREFERRED_URL_SCHEME = os.environ.get('FLASK_PREFERRED_URL_SCHEME', 'http')

# DATABASE
POSTGRES_USER = os.environ.get('POSTGRES_USER', 'qualitas')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'qualitas')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'db')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT', '5432')
POSTGRES_DB = os.environ.get('POSTGRES_DB', 'qualitas_db')
DATABASE_URL = os.environ.get('DATABASE_URL', None)  # DATABASE URL SET BY HEROKU

if DATABASE_URL:
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
else:
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"
    )
SQLALCHEMY_TRACK_MODIFICATIONS = False

# GITHUB
GITHUB_USER = os.environ.get('GITHUB_USER', None)
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
