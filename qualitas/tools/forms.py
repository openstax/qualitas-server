from flask_wtf import FlaskForm

from wtforms import SelectField, StringField, HiddenField
from wtforms.validators import DataRequired, Length

from qualitas.admin.data import get_tutor_repos, CNX_HOSTS

TUTOR_REPOS = get_tutor_repos()
TUTOR_REPOS.sort()


class PullRequestExportForm(FlaskForm):
    repo_1 = SelectField('Repository', choices=[(x, x) for x in TUTOR_REPOS])
    base_1 = StringField('Base', validators=[Length(min=7, max=40), DataRequired()])
    head_1 = StringField('Head', validators=[Length(min=7, max=40), DataRequired()])
    view_data = HiddenField(default='off')


class ServerDiffForm(FlaskForm):
    server_1 = SelectField('Server 1', choices=[(x, x) for x in CNX_HOSTS])
    server_2 = SelectField('Server 2', choices=[(x, x) for x in CNX_HOSTS])
