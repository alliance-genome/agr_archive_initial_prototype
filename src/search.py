def build_es_aggregation_body_request(es_query, category, category_filters):
    agg_query_body = {
        'query': es_query,
        'size': 0,
        'aggs': {}
    }

    if category == '':
        agg_query_body['aggs'] = {
            'categories': {
                'terms': {'field': 'category', 'size': 50}
            }
        }
    elif category in category_filters.keys():
        for subcategory in category_filters[category]:
            agg_query_body['aggs'][subcategory] = {
                'terms': {
                    'field': subcategory + '.raw',
                    'size': 999
                }
            }
    else:
        return {}

    return agg_query_body


def format_aggregation_results(aggregation_results, category, category_filters):
    if category == '':
        category_obj = {
            'values': [],
            'key': 'category'
        }

        for bucket in aggregation_results['aggregations']['categories']['buckets']:
            category_obj['values'].append({
                'key': bucket['key'],
                'total': bucket['doc_count']
            })

        return [category_obj]
    elif category in category_filters.keys():
        formatted_agg = []

        for subcategory in category_filters[category]:
            agg_obj = {
                'key': subcategory,
                'values': []
            }

            if subcategory in aggregation_results['aggregations']:
                for agg in aggregation_results['aggregations'][subcategory]['buckets']:
                    agg_obj['values'].append({
                        'key': agg['key'],
                        'total': agg['doc_count']
                    })
            formatted_agg.append(agg_obj)

        return formatted_agg
    else:
        return []


def build_es_search_body_request(query, category, es_query, json_response_fields, search_fields, sort_by):
    es_search_body = {
        '_source': json_response_fields,
        'highlight': {
            'fields': {}
        },
        'query': {}
    }

    if query == '' and category == '':
        es_search_body["query"] = {
            "function_score": {
                "query": es_query,
                "random_score": {"seed": 12345}
            }
        }
    else:
        es_search_body["query"] = es_query

    for field in search_fields:
        es_search_body['highlight']['fields'][field] = {}

    if sort_by == 'alphabetical':
        es_search_body['sort'] = [
            {
                "name.raw": {
                    "order": "asc"
                }
            }
        ]

    return es_search_body


def build_search_query(query, fields, category, category_filters, args):
    es_query = build_search_params(query, fields)

    if category == '':
        return es_query

    query = {
        'filtered': {
            'query': es_query,
            'filter': {
                'bool': {
                    'must': [{'term': {'category': category}}]
                }
            }
        }
    }

    if category in category_filters.keys():
        for item in category_filters[category]:
            if args.get(item, None):
                query['filtered']['filter']['bool']['must'].append({
                    'term': {
                        (item + ".raw"): args.get(item)
                    }
                })

    return query


def build_search_params(query, fields):
    for special_char in ['-', '.']:
        if special_char in query:
            query = "\"" + query + "\""
            break

    if query is "":
        es_query = {"match_all": {}}
    else:
        es_query = {'dis_max': {'queries': []}}

        if (query[0] in ('"', "'") and query[-1] in ('"', "'")):
            es_query['dis_max']['queries'] = [
                {
                    "match_phrase_prefix": {
                        "name": {
                            "query": query,
                            "analyzer": "standard",
                            "boost": 10
                        }
                    }
                }, {
                    "multi_match": {
                        "query": query,
                        "type": "phrase_prefix",
                        "fields": fields,
                        "boost": 3
                    }
                }
            ]
        else:
            es_query['dis_max']['queries'] = [
                    {
                        "term": {
                            "name.simple": {
                                "value": query,
                                "boost": 100
                            }
                        }
                    },
                    {
                        "multi_match": {
                            "query": query,
                            "type": "most_fields",
                            "fields": fields + ['description', 'name.fulltext^2'],
                            "boost": 25
                        }
                    },
                    {
                        "match_phrase_prefix": {
                            "name": {
                                "query": query,
                                "analyzer": "standard",
                                "max_expansions": 30,
                                "boost": 1
                            }
                        }
                    }
                ]

    return es_query


def format_search_results(search_results, json_response_fields):
    formatted_results = []

    for r in search_results['hits']['hits']:
        raw_obj = r.get('_source')

        obj = {}
        for field in json_response_fields:
            obj[field] = raw_obj.get(field)

        obj['highlights'] = r.get('highlight')

        formatted_results.append(obj)

    return formatted_results
