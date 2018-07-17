from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

from appconfig import Config

es = Elasticsearch(Config.ELASTICSEARCH_URL)


def search_industry(search_string, search_from, search_to, filters, page_no):
    kwargs = {'search_from': search_from, 'search_to': search_to}
    return search_field(search_string, filters, page_no, 'IndustryCode', **kwargs)


def search_postcode(search_string, filters, page_no):
    return search_field(search_string, filters, page_no, 'PostCode')


def search_name(search_string, filters, page_no):
    return search_field(search_string, filters, page_no, 'BusinessName')


def search_all(search_string, filters, page_no):
    return search_field(search_string, filters, page_no, 'ALL')


def search_ubrn(search_string, filters, page_no):
    return search_field(search_string, filters, page_no, 'UBRN')


def search_crn(search_string, filters, page_no):
    return search_field(search_string, filters, page_no, 'CompanyNo')


def search_vat(search_string, filters, page_no):
    return search_field(search_string, filters, page_no, 'VatRefs')


def search_paye(search_string, filters, page_no):
    return search_field(search_string, filters, page_no, 'PayeRefs')


def search_field(search_string, filters, page_no, field, **kwargs):
    if kwargs is not None:
        search_from = kwargs.get('search_from')
        search_to = kwargs.get('search_to')

        if search_from or search_to:
            search_string = "*"

    start = page_no * Config.ITEMS_PER_PAGE - Config.ITEMS_PER_PAGE

    orig_search_string = search_string

    try:
        search_string = check_reserved_characters(search_string)
    except AttributeError:
        pass

    if field == 'ALL':
        s = Search(using=es, index=Config.INDEX) \
            .query("query_string", query=search_string)
    else:
        s = Search(using=es, index=Config.INDEX) \
            .query("simple_query_string", query=search_string, fields=[field])

    s = s[start:page_no * Config.ITEMS_PER_PAGE]

    filters_active = 'None'

    employment_toggle = filters.get('employment-toggle', None)
    if employment_toggle:
        filters_active = "Employment"
        s = s.filter('terms', EmploymentBands=populate_filter(employment_toggle))

    turnover_toggle = filters.get('turnover-toggle', None)
    if turnover_toggle:
        if filters_active != 'None':
            filters_active += ', Turnover'
        else:
            filters_active = 'Turnover'
        filters_active += ' Turnover'
        s = s.filter('terms', Turnover=populate_filter(turnover_toggle))

    trading_toggle = filters.get('trading-toggle', None)
    if trading_toggle:
        if filters_active != 'None':
            filters_active += ', Trading'
        else:
            filters_active = 'Trading'
        s = s.filter('terms', TradingStatus=populate_filter(trading_toggle))

    search_from = kwargs.get('search_from')
    search_to = kwargs.get('search_to')

    if search_from or search_to:
        s = s.filter('range', IndustryCode={'gte': int(search_from) - 1, 'lt': int(search_to) + 1})
        s = s.sort('IndustryCode')

    legal_toggle = filters.get('legal-toggle', None)
    if legal_toggle:
        legal_toggle_rep = []
        legal_map = {'Company': '1', 'Sole Proprietor': 2, 'Partnership': 3, 'Public Corporation': 4,
                     'Central Government': 5, 'Local Authority': 6,
                     'Non-Profit Organisation': 7, 'Charity': 8}
        for n, i in enumerate(legal_toggle):
            legal_toggle_rep.append(str(legal_map.get(i)))

        s = s.filter('terms', LegalStatus=legal_toggle_rep)
        if filters_active != 'None':
            filters_active += ', Legal Status'
        else:
            filters_active = 'Legal Status'

    print(s.to_dict())

    res = s.execute()

    res['hits']['items_found'] = res['hits']['total']

    if res['hits']['total'] > Config.MAX_ITEMS_RETURNED:
        res['hits']['total'] = Config.MAX_ITEMS_RETURNED

    if res['hits']['total'] > Config.ITEMS_PER_PAGE:
        res['hits']['paging_active'] = True
    else:
        res['hits']['paging_active'] = False

    res['hits']['search_string'] = orig_search_string
    res['hits']['filters_active'] = filters_active

    substutite_values(res['hits'])

    return res['hits']


def substutite_values(items):
    bands = {
        'A': '0', 'B': '1', 'C': '2-4', 'D': '5-9',
        'E': '10-19', 'F': '20-24', 'G': '25-49',
        'H': '50-74', 'I': '75-99', 'J': '100-149',
        'K': '150-199', 'L': '200-249', 'M': '250-299',
        'N': '300-499', 'O': '500+'
    }

    turnover = {
        'A': '0-99', 'B': '100-249', 'C': '250-499',
        'D': '500-999', 'E': '1,000-1,999', 'F': '2,000-4,999',
        'G': '5,000-9,999', 'H': '10,000-49,999', 'I': '50,000+'
    }

    trading = {'A': 'Active', 'C': 'Closed', 'D': 'Dormant', 'I': 'Insolvent'}

    legal = {1: 'Company', 2: 'Sole Proprietor', 3: 'Partnership', 4: 'Public Corporation',
             5: 'Central Government', 6: 'Local Authority',
             7: 'Non-Profit Organisation', 8: 'Charity'
             }

    for item in items['hits']:
        item['_source']['EmploymentBands'] = bands[item['_source']['EmploymentBands']]
        item['_source']['TradingStatus'] = trading[item['_source']['TradingStatus']]
        item['_source']['Turnover'] = turnover[item['_source']['Turnover']]
        item['_source']['LegalStatus'] = legal[item['_source']['LegalStatus']]


def populate_filter(toggle):
    # Take the first character of the description (the value of the item in the filter).
    # This works for everything except legal status
    # where we have to do a substitution as seen above

    a = []
    for v in toggle[:-1]:
        a.append(v[0])
    a.append(toggle[-1][0])
    return a


def check_reserved_characters(string):
    # check for and escape
    reserved = ['"', '\', ' + ', "'""]
    for tag in reserved:
        string = string.replace(tag, '\\' + tag)
    return string
