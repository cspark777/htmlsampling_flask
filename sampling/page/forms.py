from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField
from wtforms.validators import DataRequired

class HtmlForm(FlaskForm):
    html_key = StringField('Key', validators=[DataRequired()])
    html = TextAreaField('HTML')
    submit = SubmitField('Submit')