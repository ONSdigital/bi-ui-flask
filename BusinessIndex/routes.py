from flask import render_template, request, url_for, abort, session
from flask_wtf import Form

from BusinessIndex import app
import forms
import search
from appconfig import Config
from pagination import Pagination
import json

tabs = [
    {'name': 'All Fields', 'href': '/index', 'active': True},
    {'name': 'Name', 'href': '/name', 'active': False},
    {'name': 'Post Code', 'href': '/postcode', 'active': False},
    {'name': 'SIC', 'href': '/industrycode', 'active': False},
    {'name': 'UBRN', 'href': '/ubrn', 'active': False},
    {'name': 'CRN', 'href': '/crn', 'active': False},
    {'name': 'VAT', 'href': '/vat', 'active': False},
    {'name': 'PAYE', 'href': '/paye', 'active': False}
]


def set_active(tab):
    for t in tabs:
        if t['name'] == tab:
            t['active'] = True
        else:
            t['active'] = False


@app.route('/')
@app.route('/index')
def index():
    form = forms.AllSearchForm()
    set_active('All Fields')
    return render_template('index.html', form=form, tabs=tabs)


@app.route('/name')
def name():
    form = forms.NameSearchForm()
    set_active('Name')
    return render_template('name.html', form=form, tabs=tabs)


@app.route('/postcode')
def postcode():
    form = forms.PostcodeSearchForm()
    set_active('Post Code')
    return render_template('postcode.html', form=form, tabs=tabs)


@app.route('/industrycode')
def industrycode():
    form = forms.IndustrycodeSearchForm()
    set_active('SIC')
    return render_template('industrycode.html', form=form, tabs=tabs)


@app.route('/search_all/', defaults={'page': 1}, methods=['GET', 'POST'])
@app.route('/search_all/page/<int:page>', methods=['GET', 'POST'])
def show_all_results(page):
    form = forms.AllSearchForm()
    search_string = form.search.data

    # keep copies in the session as next pages don't have the search string and filters available
    # in the form

    if search_string is None:
        search_string = session['search_string']
        filters = session['filters']
    else:
        session['search_string'] = search_string
        filters = json.loads(form.search_all_filters.data)
        session['filters'] = filters

    results = search.search_all(search_string, filters, page)

    count = results['total']

    if not results and page != 1:
        abort(404)

    pagination = Pagination(page, Config.ITEMS_PER_PAGE, count)
    return render_template('results.html', pagination=pagination, companies=results, tabs=tabs)


@app.route('/search_name/', defaults={'page': 1}, methods=['GET', 'POST'])
@app.route('/search_name/page/<int:page>', methods=['GET', 'POST'])
def show_name_results(page):
    form = forms.NameSearchForm()
    search_string = form.search.data

    if search_string is None:
        search_string = session['search_string']
        filters = session['filters']
    else:
        session['search_string'] = search_string
        filters = json.loads(form.search_name_filters.data)
        session['filters'] = filters

    results = search.search_name(search_string, filters, page)

    count = results['total']

    if not results and page != 1:
        abort(404)

    pagination = Pagination(page, Config.ITEMS_PER_PAGE, count)
    return render_template('results.html', pagination=pagination, companies=results, tabs=tabs)


@app.route('/search_postcode/', defaults={'page': 1}, methods=['GET', 'POST'])
@app.route('/search_postcode/page/<int:page>', methods=['GET', 'POST'])
def show_postcode_results(page):
    form = forms.PostcodeSearchForm()
    search_string = form.search.data

    if search_string is None:
        search_string = session['search_string']
        filters = session['filters']
    else:
        session['search_string'] = search_string
        filters = json.loads(form.search_postcode_filters.data)
        session['filters'] = filters

    results = search.search_postcode(search_string, filters, page)

    count = results['total']

    if not results and page != 1:
        abort(404)

    pagination = Pagination(page, Config.ITEMS_PER_PAGE, count)
    return render_template('results.html', pagination=pagination, companies=results, tabs=tabs)


@app.route('/search_industry/', defaults={'page': 1}, methods=['GET', 'POST'])
@app.route('/search_industry/page/<int:page>', methods=['GET', 'POST'])
def show_industry_results(page):
    form = forms.IndustrycodeSearchForm(request.form)
    search_string = form.search.data
    checkbox = form.checkbox.data
    search_from = form.searchfrom.data
    search_to = form.searchto.data

    if page == 1:
        if not form.validate_on_submit():
            #  pass the checkbox so we can show the correct from/to pane
            return render_template('industrycode.html', form=form, tabs=tabs, visible=checkbox)

    if page == 1:
        session['search_string'] = search_string
        filters = json.loads(form.search_industry_filters.data)
        session['filters'] = filters
        session['checkbox'] = checkbox
        session['search_from'] = search_from
        session['search_to'] = search_to
    else:
        search_string = session['search_string']
        filters = session['filters']
        checkbox = session['checkbox']
        search_from = session['search_from']
        search_to = session['search_to']

    results = search.search_industry(search_string, search_from,  search_to, filters, page)

    count = results['total']

    if not results and page != 1:
        abort(404)

    pagination = Pagination(page, Config.ITEMS_PER_PAGE, count)
    return render_template('results.html', pagination=pagination, companies=results, tabs=tabs)


def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)


app.jinja_env.globals['url_for_other_page'] = url_for_other_page
