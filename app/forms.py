from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, IntegerField
from wtforms import validators
from wtforms.validators import DataRequired, NumberRange

class IntForm(FlaskForm):
    criteria = IntegerField('School Id', validators=[])
    strCriteria = StringField('string', validators=[])
    search    =  SubmitField('Search')
    
