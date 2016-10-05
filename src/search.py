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
