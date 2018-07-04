from flask import redirect, render_template, request, url_for
from BusinessIndex import app
from forms import SearchForm


@app.route('/')
@app.route('/index')
def hello_world():
    form = SearchForm()
    return render_template('index.html', form=form)


@app.route('/search', methods=['GET', 'POST'])
def search_form_post():
    form = SearchForm()
    print("Searching for: " + form.search.data)
    return render_template('index.html', form=form)

