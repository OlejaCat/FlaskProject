from flask_wtf import FlaskForm
from wtforms import SubmitField


class ClearProductForm(FlaskForm):
    submit = SubmitField('Clear')