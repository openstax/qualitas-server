from flask_babel import Babel
from flask_security import Security
from flask_sqlalchemy import SQLAlchemy

# Instantiate Extensions
babel = Babel()
db = SQLAlchemy()
security = Security()

