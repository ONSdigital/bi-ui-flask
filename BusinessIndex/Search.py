
from elasticsearch import Elasticsearch
import json

es = Elasticsearch(['http://localhost:9200'])


def search(search_string):
    query = json.dumps({
        "from": 0, "size": 10,
        "query": {
            "query_string": {
                "query": search_string,
                "fields": ["_all"]
            }
        }
    })

    res = es.search(index="bi", body=query)
    print("Got %d Hits:" % res['hits']['total'])
    return res['hits']
    # for hit in res['hits']['hits']:
    #     print("%(BusinessName)s %(CompanyNo)s: %(text)s" % hit["_source"])