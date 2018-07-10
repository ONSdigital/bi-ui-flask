from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class AllSearchForm(FlaskForm):
    search = StringField('Enter Search Criteria', validators=[DataRequired()])
    submit = SubmitField('Search')


class NameSearchForm(FlaskForm):
    search = StringField('Enter Search Criteria', validators=[DataRequired()])
    submit = SubmitField('Search')


class PostcodeSearchForm(FlaskForm):
    search = StringField('Enter Search Criteria', validators=[DataRequired()])
    submit = SubmitField('Search')
