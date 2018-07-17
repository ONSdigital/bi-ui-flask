from flask_wtf import FlaskForm, Form
from wtforms import StringField, SubmitField, HiddenField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length


class AllSearchForm(FlaskForm):
    search = StringField(u'Enter Search Criteria', validators=[DataRequired(message=u'Search term required')])
    submit = SubmitField(u'Search')
    search_all_filters = HiddenField()


class NameSearchForm(FlaskForm):
    search = StringField(u'Enter Search Criteria', validators=[DataRequired(message=u'Business name required')])
    submit = SubmitField(u'Search')
    search_name_filters = HiddenField()


class PostcodeSearchForm(FlaskForm):
    search = StringField(u'Enter Post Code:', validators=[DataRequired(message=u'Post Code required')])
    submit = SubmitField(u'Search')
    search_postcode_filters = HiddenField()


class IndustrycodeSearchForm(FlaskForm):
    checkbox = BooleanField(u'Search Range', validators=[DataRequired()])
    search = IntegerField(u'Enter SIC Code:', validators=[Length(min=4)])
    searchfrom = IntegerField(u'From:', validators=[Length(min=4)])
    searchto = IntegerField(u'To:', validators=[Length(min=4)])
    submit = SubmitField(u'Search')
    search_industry_filters = HiddenField()

    def validate(self):
        result = True
        if self.checkbox.data:
            if not self.searchfrom.data:
                a = list(self.searchfrom.errors)
                a.append('From value required (integer)')
                self.searchfrom.errors = tuple(a)
                self.searchfrom.data = None
                self.searchto.data = None
                result = False
            elif not self.searchto.data:
                a = list(self.searchto.errors)
                a.append('To value required (integer)')
                self.searchto.errors = tuple(a)
                self.searchfrom.data = None
                self.searchto.data = None
                result = False
            elif self.searchto.data < self.searchfrom.data:
                a = list(self.searchto.errors)
                a.append('To value be >= the from value')
                self.searchto.errors = tuple(a)
                self.searchfrom.data = None
                self.searchto.data = None
                result = False
        else:
            if not self.search.data:
                a = list(self.search.errors)
                a.append('Search value required (integer)')
                self.search.errors = tuple(a)
                result = False

        return result


class UBRNSearchForm(FlaskForm):
    search = StringField(u'Enter UBRN Number:', validators=[DataRequired(message=u'UBRN number required')])
    submit = SubmitField(u'Search')
    search_ubrn_filters = HiddenField()


class CRNSearchForm(FlaskForm):
    search = StringField(u'Enter Company Identifier:', validators=[DataRequired(message=u'Company identifier required')])
    submit = SubmitField(u'Search')
    search_crn_filters = HiddenField()


class VATSearchForm(FlaskForm):
    search = StringField(u'Enter VAT Number:', validators=[DataRequired(message=u'VAT Number required')])
    submit = SubmitField(u'Search')
    search_vat_filters = HiddenField()


class PAYESearchForm(FlaskForm):
    search = StringField(u'Enter PAYE Number:', validators=[DataRequired(message=u'PAYE number required')])
    submit = SubmitField(u'Search')
    search_paye_filters = HiddenField()

