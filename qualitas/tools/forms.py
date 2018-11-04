from flask_wtf import FlaskForm

from wtforms import SelectField, StringField, validators
from wtforms.validators import DataRequired, Length


# List of Tutor Products
TUTOR_REPOS = [
    'openstax/accounts',
    'openstax/exercises',
    'openstax/payments',
    'openstax/tutor-js',
    'openstax/openstax-cms',
    'openstax/os-webview',
    'openstax/biglearn-api',
    'openstax/biglearn-local-query',
    'openstax/biglearn-scheduler',
    'openstax/hypothesis-deployment',
    'openstax/hypothesis-server',
    'openstax/oscms-deployment',
    'openstax/ospayments-deployment',
    'openstax/tutor-deployment',
    'openstax/tutor-server'
]

CNX_HOSTS = [
    'https://cnx.org',
    'https://qa.cnx.org',
    'https://staging.cnx.org',
    'https://devb.cnx.org',
    'https://content01.cnx.org'
]


class PullRequestExportForm(FlaskForm):
    repo_1 = SelectField('Repository', choices=[(x, x) for x in TUTOR_REPOS])
    base_1 = StringField('Base', validators=[Length(min=7, max=40), DataRequired()])
    head_1 = StringField('Head', validators=[Length(min=7, max=40), DataRequired()])


class ServerDiffForm(FlaskForm):
    server_1 = SelectField('Server 1', choices=[(x, x) for x in CNX_HOSTS])
    server_2 = SelectField('Server 2', choices=[(x, x) for x in CNX_HOSTS])
