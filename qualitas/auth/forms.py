from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired

from qualitas.auth.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])

    def validate_username(self, field):
        self.user = User.gh_load(field.data)
