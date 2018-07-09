from elasticsearch import Elasticsearch
from appconfig import Config
import json

es = Elasticsearch(['http://localhost:9200'])


def search(search_string, page_no):
    start = page_no * Config.ITEMS_PER_PAGE - Config.ITEMS_PER_PAGE

    search_string = check_reserved(search_string)

    query = json.dumps({
        "from": start, "size": Config.ITEMS_PER_PAGE,
        "query": {
            "simple_query_string": {
                "query": search_string,

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

    return res['hits']


def check_reserved(string):
    # check for and escape
    reserved = ['"', '\', ' + ', "'""]
    for tag in reserved:
        string = string.replace(tag, '\\' + tag)
    print('Search String: ' + string)
    return string
