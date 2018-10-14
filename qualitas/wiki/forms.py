from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, HiddenField
from wtforms.validators import DataRequired


class CreateWikiForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    text = TextAreaField('Text', validators=[])


class EditWikiForm(CreateWikiForm):
    id = HiddenField()
    draft = BooleanField()
    public = BooleanField()
