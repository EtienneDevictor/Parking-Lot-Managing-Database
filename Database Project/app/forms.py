from flask_wtf import FlaskForm
from sqlalchemy import Integer
from wtforms import StringField, BooleanField, SubmitField, FieldList, FormField
from wtforms import validators
from wtforms.validators import DataRequired, NumberRange

class PermitHolderForm(FlaskForm):
    school_id = StringField('School Id', validators=[DataRequired()])