from elasticsearch import Elasticsearch
from appconfig import Config
import json

es = Elasticsearch(Config.ELASTICSEARCH_URL)


def search_postcode(search_string, filters, page_no):
    return search_field(search_string, filters, 'PostCode', page_no)


def search_name(search_string, filters, page_no):
    return search_field(search_string, filters, 'BusinessName', page_no)


def search_all(search_string, filters, page_no):
    return search_field(search_string, filters, 'ALL', page_no)


def search_field(search_string, filters, field, page_no):
    start = page_no * Config.ITEMS_PER_PAGE - Config.ITEMS_PER_PAGE

    orig_search_string = search_string
    search_string = check_reserved_characters(search_string)

    filter_string = add_filters(filters)

    print('query: ' + search_string + ' ' + filter_string)

    if field == 'ALL':

        query = json.dumps({
            "from": start, "size": Config.ITEMS_PER_PAGE,
            "query": {
                "simple_query_string": {
                    "query": search_string + ' ' + filter_string
                }
            }
        })

    else:

        query = json.dumps({
            "from": start, "size": Config.ITEMS_PER_PAGE,
            "query": {
                "simple_string": {
                    "query": search_string,
                    "fields": [field],
                }
            }
        })

    res = es.search(index=Config.INDEX, body=query)
    res['hits']['items_found'] = res['hits']['total']

    if res['hits']['total'] > Config.MAX_ITEMS_RETURNED:
        res['hits']['total'] = Config.MAX_ITEMS_RETURNED

    if res['hits']['total'] > Config.ITEMS_PER_PAGE:
        res['hits']['paging_active'] = True
    else:
        res['hits']['paging_active'] = False

    res['hits']['search_string'] = orig_search_string

    return res['hits']


def check_reserved_characters(string):
    # check for and escape
    reserved = ['"', '\', ' + ', "'""]
    for tag in reserved:
        string = string.replace(tag, '\\' + tag)
    return string


def add_filters(filters):

    filter_methods = {
        'employment-toggle': _employment_filter,
        'turnover-toggle': _turnover_filter,
        'trading-toggle': _trading_filter,
        'legal-toggle': _legal_filter
    }

    filter_string = ''

    for k in filters:
        filter_string += filter_methods[k](filters[k])

    return filter_string


def _employment_filter(items):
    r = 'AND EmploymentBands:('
    for v in items[:-1]:
        r += v[0] + " AND "
    r += items[-1][0] + ")"
    return r


def _turnover_filter(items):
    for v in items:
        print(' value: ' + v[0])
    return ''


def _trading_filter(items):
    for v in items:
        print(' value: ' + v)
    return ''


def _legal_filter(items):
    for v in items:
        print(' value: ' + v)
    return ''
