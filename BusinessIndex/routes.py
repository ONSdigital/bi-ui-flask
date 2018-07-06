from flask import render_template, request, url_for, abort, session
from BusinessIndex import app
from forms import SearchForm
from search import search
from config import Config
from pagination import Pagination


@app.route('/')
@app.route('/index')
def index():
    form = SearchForm()
    return render_template('index.html', form=form)


@app.route('/search/', defaults={'page': 1}, methods=['GET', 'POST'])
@app.route('/search/page/<int:page>', methods=['GET', 'POST'])
def show_results(page):
    form = SearchForm()
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
