
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


def format_aggregation_results(aggregation_results,
                               category,
                               category_filters):
    aggs = aggregation_results.get('aggregations', {})
    if category == '':
        category_obj = {
            'values': [],
            'key': 'category'
        }

        for bucket in aggs['categories']['buckets']:
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

            if subcategory in aggs:
                for agg in aggs[subcategory]['buckets']:
                    agg_obj['values'].append({
                        'key': agg['key'],
                        'total': agg['doc_count']
                    })
            formatted_agg.append(agg_obj)

        return formatted_agg
    else:
        return []


def build_es_search_body_request(query,
                                 category,
                                 es_query,
                                 json_response_fields,
                                 search_fields,
                                 sort_by):
    es_search_body = {
        '_source': json_response_fields,
        'highlight': {
            'fields': {}
        },
        'query': {}
    }

    if query == '' and category == '':
        es_search_body['query'] = {
            'function_score': {
                'query': es_query,
                'random_score': {'seed': 12345}
            }
        }
    else:
        es_search_body['query'] = es_query

    for field in search_fields:
        es_search_body['highlight']['fields'][field] = {}

    if sort_by == 'alphabetical':
        es_search_body['sort'] = [
            {
                'name.raw': {
                    'order': 'asc'
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
            for param in args.getlist(item, None):
                query['filtered']['filter']['bool']['must'].append({
                    'term': {
                        (item + '.raw'): param
                    }
                })

    return query


def build_search_params(query, fields,
                        quote_chars=('"', "'")):
    for special_char in ['-', '.']:
        if special_char in query:
            query = '"' + query + '"'
            break

    if query == '':
        es_query = {'match_all': {}}
    else:
        es_query = {'dis_max': {'queries': []}}

        if query.startswith(quote_chars) or query.endswith(quote_chars):
            es_query['dis_max']['queries'] = [
                {
                    'match_phrase_prefix': {
                        'name': {
                            'query': query,
                            'analyzer': 'standard',
                            'boost': 10
                        }
                    }
                }, {
                    'multi_match': {
                        'query': query,
                        'type': 'phrase_prefix',
                        'fields': fields,
                        'boost': 3
                    }
                }
            ]
        else:
            es_query['dis_max']['queries'] = [{
                'term': {
                    'name.simple': {
                        'value': query,
                        'boost': 100
                    }
                }
            }, {
                'multi_match': {
                    'query': query,
                    'type': 'most_fields',
                    'fields': fields + [
                        'description',
                        'name.fulltext^2'
                    ],
                    'boost': 25
                }
            }, {
                'match_phrase_prefix': {
                    'name': {
                        'query': query,
                        'analyzer': 'standard',
                        'max_expansions': 30,
                        'boost': 1
                    }
                }
            }]
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


def build_autocomplete_search_body_request(query,
                                           category='gene',
                                           field='name'):
    es_query = {
        'query': {
            'bool': {
                'must': [{
                    'match': {
                        'name': {
                            'query': query,
                            'analyzer': 'standard'
                        }
                    }
                }],
                'should': [
                    {
                        'match': {
                            'category': {
                                'query': 'gene',
                                'boost': 4
                            }
                        }
                    }
                ]
            }
        },
        '_source': ['name', 'href', 'category']
    }

    if category != '':
        q_bool = es_query['query']['bool']
        q_bool['must'].append({'match': {'category': category}})
        if category != 'gene':
            q_bool.pop('should')

    if field != 'name':
        es_query['aggs'] = {}
        es_query['aggs'][field] = {
            'terms': {'field': field + '.raw', 'size': 999}
        }

        q_bool_match = {
            field + '.autocomplete': {
                'query': query,
                'analyzer': 'standard'
            }
        }
        q_bool['must'][0]['match'] = q_bool_match
        es_query['_source'] = [field, 'href', 'category']

    return es_query


def format_autocomplete_results(es_response, field='name'):
    formatted_results = []

    if field != 'name':
        results = es_response['aggregations'][field]['buckets']
        for r in results:
            obj = {
                'name': r['key']
            }
            formatted_results.append(obj)
    else:
        for hit in es_response['hits']['hits']:
            obj = {
                'name': hit['_source']['name'],
                'href': hit['_source']['href'],
                'category': hit['_source']['category']
            }
            formatted_results.append(obj)

    return formatted_results
