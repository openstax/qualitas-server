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


class PullRequestExportForm(FlaskForm):
    repo_1 = SelectField('Repository', choices=[(x, x) for x in TUTOR_REPOS])
    base_1 = StringField('Base', validators=[Length(min=7, max=40), DataRequired()])
    head_1 = StringField('Head', validators=[Length(min=7, max=40), DataRequired()])
