
from elasticsearch import Elasticsearch
from config import Config
import json

es = Elasticsearch(['http://localhost:9200'])


def search(search_string, page_no):

    start = page_no * Config.ITEMS_PER_PAGE - Config.ITEMS_PER_PAGE

    query = json.dumps({
        "from": start, "size": Config.ITEMS_PER_PAGE,
        "query": {
            "query_string": {
                "query": search_string,
                "fields": ["_all"]
            }
        }
    })

    res = es.search(index="test", body=query)
    res['hits']['items_found'] = res['hits']['total']

    if res['hits']['total'] > Config.MAX_ITEMS_RETURNED:
        res['hits']['total'] = Config.MAX_ITEMS_RETURNED

    if res['hits']['total'] > Config.ITEMS_PER_PAGE:
        res['hits']['paging_active'] = True
    else:
        res['hits']['paging_active'] = False


    return res['hits']

