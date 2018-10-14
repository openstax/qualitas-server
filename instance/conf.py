import os
import uuid

from qualitas.utils import make_database_url


# SETTINGS

# MAIN FLASK APPLICATION
DEBUG = os.environ.get('FLASK_DEBUG', False)
SECRET_KEY = os.environ.get('SESSION_SECRET', str(uuid.uuid4()))
SQLALCHEMY_DATABASE_URI = make_database_url()
SQLALCHEMY_TRACK_MODIFICATIONS = False

# GITHUB
GITHUB_USER = os.environ.get('GITHUB_USER', None)
GITHUB_PASSWORD = os.environ.get('GITHUB_PASSWORD', None)
GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID', None)
GITHUB_SECRET = os.environ.get('GITHUB_SECRET', None)
