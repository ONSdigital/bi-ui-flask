from elasticsearch import Elasticsearch
from appconfig import Config
import json

es = Elasticsearch(Config.ELASTICSEARCH_URL)


def search_postcode(search_string, page_no):
    return search_field(search_string, 'PostCode', page_no)


def search_name(search_string, page_no):
    return search_field(search_string, 'BusinessName', page_no)


def search_all(search_string, page_no):
    return search_field(search_string, 'ALL', page_no)


def search_field(search_string, field, page_no):
    start = page_no * Config.ITEMS_PER_PAGE - Config.ITEMS_PER_PAGE

    orig_search_string = search_string
    search_string = check_reserved_characters(search_string)

    if field == 'ALL':

        query = json.dumps({
            "from": start, "size": Config.ITEMS_PER_PAGE,
            "query": {
                "simple_query_string": {
                    "query": search_string,
                }
            }
        })

    else:

        query = json.dumps({
            "from": start, "size": Config.ITEMS_PER_PAGE,
            "query": {
                "simple_query_string": {
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
    print('Search String: ' + string)
    return string
