from flask import render_template, request, url_for, abort, session
from BusinessIndex import app
import forms
from search import search
from appconfig import Config
from pagination import Pagination

tabs = [
    {'name': 'All Fields', 'href': '/index', 'active': True},
    {'name': 'Name', 'href': '/name', 'active': True},
    {'name': 'Post Code', 'href': '/postcode', 'active': False},
    {'name': 'SIC', 'href': '/sic', 'active': False},
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


@app.route('/postcode')
def postcode():
    form = forms.PostcodeSearchForm()
    set_active('Post Code')
    return render_template('postcode.html', form=form, tabs=tabs)


@app.route('/name')
def name():
    form = forms.NameSearchForm()
    set_active('Name')
    return render_template('name.html', form=form, tabs=tabs)


@app.route('/search_all/', defaults={'page': 1}, methods=['GET', 'POST'])
@app.route('/search_all/page/<int:page>', methods=['GET', 'POST'])
def show_results(page):
    form = forms.AllSearchForm()
    search_string = form.search.data

    if search_string is None:
        search_string = session['search_string']
    else:
        session['search_string'] = search_string

    results = search(search_string, page)
    count = results['total']
    if not results and page != 1:
        abort(404)
    pagination = Pagination(page, Config.ITEMS_PER_PAGE, count)
    return render_template('results.html', pagination=pagination, companies=results)


def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)


app.jinja_env.globals['url_for_other_page'] = url_for_other_page
