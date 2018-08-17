import os
import uuid

import redis

from qualitas.utils import make_database_url


# SETTINGS

# MAIN FLASK APPLICATION
DEBUG = os.environ.get('FLASK_DEBUG', False)
SECRET_KEY = os.environ.get('SESSION_SECRET', str(uuid.uuid4()))

# REDIS
# SESSION_TYPE = 'redis'
# REDIS_URL = os.environ.get('REDISTOGO_URL', None)
# SESSION_REDIS = redis.from_url(REDIS_URL)

# GITHUB

GITHUB_USER = os.environ.get('GITHUB_USER', None)
GITHUB_PASSWORD = os.environ.get('GITHUB_PASSWORD', None)
