from flask_wtf import Flaskform
from wtforms import StringField, BooleanField, SubmitField, IntegerField
from wtforms import validators
from wtforms.validators import DataRequired, NumberRange

class PermitHolderForm(FlaskForm):
    school_id = IntegerField('School Id', validators=[DataRequired()])