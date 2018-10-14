from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired

from qualitas.auth.models import User


class LoginForm(FlaskForm):
    user_id = StringField('User ID', validators=[InputRequired()])

    def validate_user_id(self, field):
        self.user = User.gh_load(field.data)
