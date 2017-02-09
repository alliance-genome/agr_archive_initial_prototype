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


def build_search_query(query, search_fields, category, category_filters, args):
    es_query = build_search_params(query, search_fields)

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
                        (item + ".raw"): param
                    }
                })

    return query


def build_search_params(query, search_fields):
    if query is "":
        es_query = {"match_all": {}}
    else:
        es_query = {'dis_max': {'queries': []}}

        if (query[0] in ('"', "'") and query[-1] in ('"', "'")):
            query = query[1:-1]

        es_query['dis_max']['queries'] = []

        custom_boosts = {
            "id": 120,
            "gene_symbol": 120,
            "gene_synonyms": 120,
            "name": 200,
            "name.symbol": 300,
            "gene_biological_process.symbol": 120,
            "gene_molecular_function.symbol": 120,
            "gene_cellular_component.symbol": 120
        }

        fields = search_fields + [
            "name.symbol",
            "gene_biological_process.symbol",
            "gene_molecular_function.symbol",
            "gene_cellular_component.symbol"
        ]

        for field in fields:
            match = {}
            match[field] = {
                'query': query,
                'boost': custom_boosts.get(field, 50)
            }

            partial_match = {}
            partial_match[field.split(".")[0]] = {
                'query': query
            }

            es_query['dis_max']['queries'].append({'match': match})
            es_query['dis_max']['queries'].append({'match_phrase_prefix': partial_match})

    return es_query


def filter_highlighting(highlight):
    if highlight is None:
        return None

    for k in highlight.keys():
        if k.endswith(".symbol") and k.split(".")[0] in highlight:
            if highlight[k] == highlight[k.split(".")[0]]:
                highlight.pop(k, None)
            else:
                highlight[k.split(".")[0]] = highlight[k]
                highlight.pop(k, None)
    return highlight


def format_search_results(search_results, json_response_fields):
    formatted_results = []

    for r in search_results['hits']['hits']:
        raw_obj = r.get('_source')

        obj = {}
        for field in json_response_fields:
            obj[field] = raw_obj.get(field)

        obj['highlights'] = filter_highlighting(r.get('highlight'))
        obj['id'] = r.get('_id')

        formatted_results.append(obj)

    return formatted_results


def build_autocomplete_search_body_request(query, category='gene', field='name_key'):
    es_query = {
        "query": {
            "bool": {
                "must": [{
                    "match": {
                        "name_key.autocomplete": {
                            "query": query
                        }
                    }
                }],
                "should": [
                    {
                        "match": {
                            "category": {
                                "query": "gene",
                                "boost": 2
                            }
                        }
                    }
                ]
            }
        },
        '_source': ['name', 'href', 'category', 'gene_symbol']
    }

    if category != '':
        es_query["query"]["bool"]["must"].append({"match": {"category": category}})
        if category != "gene":
            es_query["query"]["bool"].pop("should")

    if field != 'name_key':
        es_query['aggs'] = {}
        es_query['aggs'][field] = {
            'terms': {'field': field + '.raw', 'size': 999}
        }

        es_query['query']['bool']['must'][0]['match'] = {}
        es_query['query']['bool']['must'][0]['match'][field + '.autocomplete'] = {
            'query': query,
            'analyzer': 'standard'
        }

        es_query['_source'] = [field, 'href', 'category']

    return es_query


def format_autocomplete_results(es_response, field='name_key'):
    formatted_results = []

    if field != 'name_key':
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

            if hit['_source'].get('gene_symbol') and hit['_source']['category'] == "gene":
                obj['name'] = hit['_source']['gene_symbol'].upper()

            formatted_results.append(obj)

    return formatted_results


def graph_visualization(formatted_search_results):
    nodes = {}
    edges = []

    for result in formatted_search_results:
        if result["href"] not in nodes:
            nodes[result["href"]] = {
                "name": result["gene_symbol"],
                "id": result["href"],
                "species": result["species"],
                "direct": True
            }

            for homolog in result["homologs"]:
                if homolog["href"] not in nodes:
                    nodes[homolog["href"]] = {
                        "name": homolog["symbol"],
                        "id": homolog["href"],
                        "species": homolog["species"],
                        "direct": False
                    }

                edges.append({
                    "source": result["href"],
                    "target": homolog["href"]
                })

    return {
        "nodes": [nodes[k] for k in nodes],
        "edges": edges
    }
