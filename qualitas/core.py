from flask_babel import Babel
from flask_security import Security
from flask_sqlalchemy import SQLAlchemy

from qualitas.ext.flask_github import FlaskGitHub

# Instantiate Extensions
from sqlalchemy import MetaData

babel = Babel()
db = SQLAlchemy(
    metadata=MetaData(naming_convention={
        'pk': 'pk_%(table_name)s',
        'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
        'uq': 'uq_%(table_name)s_%(column_0_name)s',
        'ix': 'ix_%(table_name)s_%(column_0_name)s',
        'ck': 'ck_%(table_name)s_%(constraint_name)s',
    }),
)
github = FlaskGitHub()
security = Security()

