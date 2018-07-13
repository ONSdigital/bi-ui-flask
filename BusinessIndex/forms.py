from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired


class AllSearchForm(FlaskForm):
    search = StringField('Enter Search Criteria', validators=[DataRequired()])
    submit = SubmitField('Search')
    search_all_filters = HiddenField()


class NameSearchForm(FlaskForm):
    search = StringField('Enter Search Criteria', validators=[DataRequired()])
    submit = SubmitField('Search')
    search_name_filters = HiddenField()


class PostcodeSearchForm(FlaskForm):
    search = StringField('Enter Search Criteria', validators=[DataRequired()])
    submit = SubmitField('Search')
    search_postcode_filters = HiddenField()
