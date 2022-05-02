from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, IntegerField
from wtforms import validators
from wtforms.validators import DataRequired, NumberRange

class IntForm(FlaskForm):
    criteria = IntegerField('School Id', validators=[DataRequired()])
    search    =  SubmitField('Search')
    
