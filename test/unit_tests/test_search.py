import unittest
from werkzeug.datastructures import ImmutableMultiDict

from src import search

class SearchHelpersTest(unittest.TestCase):
    pass


class TestBuildSearchParams(unittest.TestCase):

    def test_should_search_for_all_with_empty_query(self):
        query = ""
        fields = ["name", "symbol"]

        self.assertEqual(search.build_search_params(query, fields), {
            "match_all": {}
        })

    def test_should_create_general_query(self):
        query = "gene"
        fields = ["name", "symbol"]

        self.assertEqual(search.build_search_params(query, fields), {
            'dis_max': {
                'queries': [
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
                            "fields": fields + [
                                'description',
                                'name.fulltext^2'
                            ],
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
            }
        })

    def test_should_quote_queries_with_special_chars(self):
        query = "eu-gene"
        fields = ["name", "symbol"]

        self.assertEqual(search.build_search_params(query, fields), {
            'dis_max': {
                'queries': [{
                    'match_phrase_prefix': {
                        'name': {
                            'analyzer': 'standard',
                            'boost': 10,
                            'query': '"' + query + '"'
                        }
                    }
                }, {
                    'multi_match': {
                        'boost': 3,
                        'fields': fields,
                        'query': '"' + query + '"',
                        'type': 'phrase_prefix'
                    }
                }]
            }
        })

    def test_should_treat_quoted_query(self):
        query = '"gene"'
        fields = ["name", "symbol"]

        self.assertEqual(search.build_search_params(query, fields), {
            'dis_max': {
                'queries': [{
                    'match_phrase_prefix': {
                        'name': {
                            'analyzer': 'standard',
                            'boost': 10,
                            'query': query
                        }
                    }
                }, {
                    'multi_match': {
                        'boost': 3,
                        'fields': fields,
                        'query': query,
                        'type': 'phrase_prefix'
                    }
                }]
            }
        })


class TestBuildSearchQuery(unittest.TestCase):

    def test_should_return_search_params_only_for_no_category(self):
        query = "gene"
        fields = ["name", "symbol"]
        category = ''
        category_filters = {
            "genes": ['go_ids', 'go_names'],
            "go": ['gene'],
        }
        args = ImmutableMultiDict()
        es_query = search.build_search_params(query, fields)
        self.assertEqual(search.build_search_query(query,
                                                   fields,
                                                   category,
                                                   category_filters,
                                                   args), es_query)

    def test_should_filter_by_category(self):
        query = "gene"
        fields = ["name", "symbol"]
        category = 'genes'
        category_filters = {
            "genes": ['go_ids', 'go_names'],
            "go": ['gene'],
        }
        args = ImmutableMultiDict()
        es_query = search.build_search_params(query, fields)
        expected_query = {
            'filtered': {
                'query': es_query,
                'filter': {
                    'bool': {
                        'must': [{'term': {'category': category}}]
                    }
                }
            }
        }
        query = search.build_search_query(query,
                                          fields,
                                          category,
                                          category_filters,
                                          args)
        self.assertEqual(query, expected_query)

    def test_should_filter_subcategories_if_passed(self):
        query = "act1"
        fields = ["name", "symbol"]
        category = "genes"
        category_filters = {
            "genes": ['go_ids', 'go_names'],
            "go": ['gene'],
        }
        args = ImmutableMultiDict([
            ('go_names', 'A'),
            ('go_names', 'B'),
            ('go_names', 'C')
        ])

        es_query = search.build_search_params(query, fields)
        expected = {
            'filtered': {
                'query': es_query,
                'filter': {
                    'bool': {
                        'must': [
                            {'term': {'category': category}},
                            {'term': {'go_names.raw': 'A'}},
                            {'term': {'go_names.raw': 'B'}},
                            {'term': {'go_names.raw': 'C'}}
                        ]
                    }
                }
            }
        }
        actual = search.build_search_query(query,
                                           fields,
                                           category,
                                           category_filters,
                                           args)
        self.assertEqual(actual, expected)


class TestBuildEsSearchBody(unittest.TestCase):

    def test_should_randomize_results_if_query_and_category_empty(self):
        query = ""
        fields = ["name", "symbol"]
        category = ""
        category_filters = {
            "genes": ['go_ids', 'go_names'],
            "go": ['gene'],
        }
        sort_by = "relevance"
        args = ImmutableMultiDict([
            ('go_names', 'A'),
            ('go_names', 'B'),
            ('go_names', 'C')
        ])
        search_fields = []
        json_response_fields = ['name', 'symbol', 'synonym']
        es_query = search.build_search_query(query,
                                             fields,
                                             category,
                                             category_filters,
                                             args)
        expected = {
            '_source': json_response_fields,
            'highlight': {
                'fields': {}
            },
            'query': {
                "function_score": {
                    "query": es_query,
                    "random_score": {"seed": 12345}
                }
            }
        }
        actual = search.build_es_search_body_request(
            query,
            category,
            es_query,
            json_response_fields,
            search_fields,
            sort_by)
        self.assertEqual(actual, expected)

    def test_should_add_highlighting(self):
        query = ""
        fields = ["name", "symbol"]
        category = ""
        category_filters = {
            "genes": ['go_ids', 'go_names'],
            "go": ['gene'],
        }
        sort_by = "relevance"
        args = ImmutableMultiDict([
            ('go_names', 'A'),
            ('go_names', 'B'),
            ('go_names', 'C')
        ])
        search_fields = ["name", "symbol"]
        json_response_fields = ['name', 'symbol', 'synonym']
        es_query = search.build_search_query(query,
                                             fields,
                                             category,
                                             category_filters,
                                             args)

        expected_response = {
            '_source': json_response_fields,
            'highlight': {
                'fields': {'name': {}, 'symbol': {}}
            },
            'query': {
                "function_score": {
                    "query": es_query,
                    "random_score": {"seed": 12345}
                }
            }
        }
        response = search.build_es_search_body_request(
            query,
            category,
            es_query,
            json_response_fields,
            search_fields,
            sort_by)
        self.assertEqual(response, expected_response)

    def test_sorts_alphabetically_by_name(self):
        query = ""
        fields = ["name", "symbol"]
        category = ""
        category_filters = {
            "genes": ['go_ids', 'go_names'],
            "go": ['gene'],
        }
        sort_by = "alphabetical"
        args = ImmutableMultiDict([
            ('go_names', 'A'),
            ('go_names', 'B'),
            ('go_names', 'C')
        ])
        search_fields = ["name", "symbol"]
        json_response_fields = ['name', 'symbol', 'synonym']
        es_query = search.build_search_query(query,
                                             fields,
                                             category,
                                             category_filters,
                                             args)
        expected_response = {
            '_source': json_response_fields,
            'highlight': {
                'fields': {'name': {}, 'symbol': {}}
            },
            'query': {
                "function_score": {
                    "query": es_query,
                    "random_score": {"seed": 12345}
                }
            },
            'sort': [
                {
                    "name.raw": {
                        "order": "asc"
                    }
                }
            ]
        }
        response = search.build_es_search_body_request(
            query,
            category,
            es_query,
            json_response_fields,
            search_fields,
            sort_by)
        self.assertEqual(response, expected_response)

    def test_should_not_randomize_results_if_category_is_defined(self):
        query = ""
        fields = ["name", "symbol"]
        category = "genes"
        category_filters = {
            "genes": ['go_ids', 'go_names'],
            "go": ['gene'],
        }
        sort_by = "alphabetical"
        args = ImmutableMultiDict([
            ('go_names', 'A'),
            ('go_names', 'B'),
            ('go_names', 'C')
        ])
        search_fields = ["name", "symbol"]
        json_response_fields = ['name', 'symbol', 'synonym']

        es_query = search.build_search_query(query,
                                             fields,
                                             category,
                                             category_filters,
                                             args)

        expected_response = {
            '_source': json_response_fields,
            'highlight': {
                'fields': {'name': {}, 'symbol': {}}
            },
            'query': es_query,
            'sort': [
                {
                    "name.raw": {
                        "order": "asc"
                    }
                }
            ]
        }
        response = search.build_es_search_body_request(
            query,
            category,
            es_query,
            json_response_fields,
            search_fields,
            sort_by)
        self.assertEqual(response, expected_response)

    def test_format_search_results(self):
        json_response_fields = ['name', 'symbol']
        search_results = {
            "took": 4,
            "timed_out": False,
            "_shards": {
                "total": 5,
                "successful": 5,
                "failed": 0
            },
            "hits": {
                "total": 120735,
                "max_score": 1.0,
                "hits": [
                    {
                        "_index": "searchable_items_prototype",
                        "_type": "searchable_item",
                        "_id": "yeast_S00001",
                        "_score": 1.0,
                        "_source": {
                            "name": "ACTin 1",
                            "symbol": "ACT1",
                            "href": "yeastgenome.org/locus/act1/overview",
                            "category": "gene"
                        }
                    }
                ]
            }
        }
        expected_results = [{
            'highlights': None,
            'name': 'ACTin 1',
            'symbol': 'ACT1'
        }]
        results = search.format_search_results(search_results,
                                               json_response_fields)
        self.assertEqual(results, expected_results)


class TestBuildEsAggregationBodyRequest(unittest.TestCase):

    def test_should_return_empty_for_invalid_category(self):
        query = ""
        fields = ["name", "symbol"]
        category = "invalid_category"
        category_filters = {
            "genes": ['go_ids', 'go_names'],
            "go": ['gene'],
        }
        args = ImmutableMultiDict([
            ('go_names', 'A'),
            ('go_names', 'B'),
            ('go_names', 'C')
        ])

        es_query = search.build_search_query(query,
                                             fields,
                                             category,
                                             category_filters,
                                             args)

        actual = search.build_es_aggregation_body_request(
            es_query, category,
            category_filters)
        self.assertEqual(actual, {})

    def test_should_aggregate_just_categories_if_empty(self):
        query = ""
        fields = ["name", "symbol"]
        category = ""
        category_filters = {
            "genes": ['go_ids', 'go_names'],
            "go": ['gene'],
        }
        args = ImmutableMultiDict([
            ('go_names', 'A'),
            ('go_names', 'B'),
            ('go_names', 'C')
        ])
        es_query = search.build_search_query(query,
                                             fields,
                                             category,
                                             category_filters,
                                             args)
        expected = {
            'query': es_query,
            'size': 0,
            'aggs': {
                'categories': {
                    'terms': {'field': 'category', 'size': 50}
                }}
        }
        actual = search.build_es_aggregation_body_request(
            es_query,
            category,
            category_filters)
        self.assertEqual(actual, expected)

    def test_should_aggregate_each_subcategory(self):
        query = ""
        fields = ["name", "symbol"]
        category = "genes"
        category_filters = {
            "genes": ['go_ids', 'go_names'],
            "go": ['gene'],
        }
        args = ImmutableMultiDict([
            ('go_names', 'A'),
            ('go_names', 'B'),
            ('go_names', 'C')
        ])

        es_query = search.build_search_query(query,
                                             fields,
                                             category,
                                             category_filters,
                                             args)
        expected = {
            'query': es_query,
            'size': 0,
            'aggs': {
                'go_ids': {
                    'terms': {'field': 'go_ids.raw', 'size': 999}
                },
                'go_names': {
                    'terms': {'field': 'go_names.raw', 'size': 999}
                }
            }
        }
        actual = search.build_es_aggregation_body_request(
            es_query,
            category,
            category_filters)
        self.assertEqual(actual, expected)



class TestFormatAggregationResults(unittest.TestCase):
    def test_should_include_all_categories_for_empty_category(self):
        category = ""
        category_filters = {
            "genes": ['go_ids', 'go_names'],
            "go": ['gene'],
        }
        aggregation_results = {
            "took": 12,
            "timed_out": False,
            "_shards": {
                "total": 5,
                "successful": 5,
                "failed": 0
            },
            "hits": {
                "total": 120735,
                "max_score": 0.0,
                "hits": []
            },
            "aggregations": {
                "categories": {
                    "doc_count_error_upper_bound": 0,
                    "sum_other_doc_count": 312,
                    "buckets": [{
                        "key": "gene",
                        "doc_count": 6691
                    }, {
                        "key": "go",
                        "doc_count": 387
                    }, {
                        "key": "diseases",
                        "doc_count": 352
                    }]
                }
            }
        }
        expected = [{
            'key': 'category',
            'values': [{
                'total': 6691,
                'key': 'gene'
            }, {
                'total': 387,
                'key': 'go'
            }, {
                'total': 352,
                'key': 'diseases'
            }]
        }]
        actual = search.format_aggregation_results(
            aggregation_results,
            category,
            category_filters)
        self.assertEqual(actual, expected)

    def test_should_include_all_subcategories(self):
        category = "genes"
        category_filters = {
            "genes": ['go_ids', 'go_names'],
            "go": ['gene'],
        }
        aggregation_results = {
            "took": 12,
            "timed_out": False,
            "_shards": {
                "total": 5,
                "successful": 5,
                "failed": 0
            },
            "hits": {
                "total": 120735,
                "max_score": 0.0,
                "hits": []
            },
            "aggregations": {
                "go_names": {
                    "doc_count_error_upper_bound": 0,
                    "sum_other_doc_count": 312,
                    "buckets": [{
                        "key": "mitochondrion",
                        "doc_count": 6691
                    }, {
                        "key": "cytoplasm",
                        "doc_count": 387
                    }, {
                        "key": "membrane",
                        "doc_count": 352
                    }]
                }
            }
        }
        expected = [{
            'key': 'go_ids',
            'values': []
        }, {
            'key': 'go_names',
            'values': [{
                'key': 'mitochondrion',
                'total': 6691
            }, {
                'key': 'cytoplasm',
                'total': 387
            }, {
                'key': 'membrane',
                'total': 352
            }]
        }]
        actual = search.format_aggregation_results(
            aggregation_results,
            category,
            category_filters)

        self.assertEqual(actual, expected)

    def test_should_return_empty_for_invalid_category(self):
        category = "invalid_category"
        category_filters = {
            "genes": ['go_ids', 'go_names'],
            "go": ['gene'],
        }
        aggregation_results = {}
        actual = search.format_aggregation_results(
            aggregation_results,
            category,
            category_filters)
        self.assertEqual(actual, [])


class TestBuildAutoCompleteSearchBody(unittest.TestCase):

    def test_default(self):
        query = "act"
        es_query = search.build_autocomplete_search_body_request(
            query, '')
        self.assertEqual(es_query, {
            "query": {
                "bool": {
                    "must": [{
                        "match": {
                            "name": {
                                "query": query,
                                "analyzer": "standard"
                            }
                        }
                    }],
                    "should": [
                        {
                            "match": {
                                "category": {
                                    "query": "gene",
                                    "boost": 4
                                }
                            }
                        }
                    ]
                }
            }, '_source': ['name', 'href', 'category']
        })

    def test_with_category(self):
        query = "act"
        es_query = search.build_autocomplete_search_body_request(
            query, 'go')
        self.assertEqual(es_query, {
            "query": {
                "bool": {
                    "must": [{
                        "match": {
                            "name": {
                                "query": query,
                                "analyzer": "standard"
                            }
                        }
                    }, {
                        "match": {"category": "go"}
                    }]
                }
            }, '_source': ['name', 'href', 'category']
        })

    def test_with_field(self):
        query = "act"
        es_query = search.build_autocomplete_search_body_request(
            query,
            'go',
            'go_id')
        self.assertEqual(es_query, {
            "query": {
                "bool": {
                    "must": [{
                        "match": {
                            "go_id.autocomplete": {
                                "query": query,
                                "analyzer": "standard"
                            }
                        }
                    }, {
                        "match": {"category": "go"}
                    }]
                }
            }, 'aggs': {
                'go_id': {
                    'terms': {'field': 'go_id.raw', 'size': 999}
                }
            }, '_source': ['go_id', 'href', 'category']
        })


class TestFormatAutoCompleteResults(unittest.TestCase):

    def test_default(self):
        es_response = {
            "took": 4,
            "timed_out": False,
            "_shards": {
                "total": 5,
                "successful": 5,
                "failed": 0
            },
            "hits": {
                "total": 3016,
                "max_score": 3.8131394,
                "hits": [{
                    "_index": "searchable_items_prototype",
                    "_type": "searchable_item",
                    "_id": "S000001855",
                    "_score": 3.8131394,
                    "_source": {
                        "name": "ACT1 / YFL039C",
                        "href": "/locus/S000001855/overview",
                        "category": "gene"
                    }
                }, {
                    "_index": "searchable_items_prototype",
                    "_type": "searchable_item",
                    "_id": "GO:0000185",
                    "_score": 0.46771955,
                    "_source": {
                        "name": "activation of MAPKKK activity",
                        "href": "/go/GO:0000185/overview",
                        "category": "go"
                    }
                }]
            }
        }

        expected = [{
            "name": "ACT1 / YFL039C",
            "href": "/locus/S000001855/overview",
            "category": "gene"
        }, {
            "name": "activation of MAPKKK activity",
            "href": "/go/GO:0000185/overview",
            "category": "go"
        }]
        actual = search.format_autocomplete_results(es_response)
        self.assertEqual(actual, expected)

    def test_with_field(self):
        es_response = {
            "took": 12,
            "timed_out": False,
            "_shards": {
                "total": 5,
                "successful": 5,
                "failed": 0
            },
            "hits": {
                "total": 120735,
                "max_score": 0.0,
                "hits": []
            },
            "aggregations": {
                "go_name": {
                    "doc_count_error_upper_bound": 0,
                    "sum_other_doc_count": 312,
                    "buckets": [{
                        "key": "cytoplasm",
                        "doc_count": 6691
                    }, {
                        "key": "nucleus",
                        "doc_count": 387
                    }, {
                        "key": "DNA repair",
                        "doc_count": 352
                    }]
                }
            }
        }
        expected = [{
            'name': "cytoplasm"
        }, {
            'name': 'nucleus'
        }, {
            'name': 'DNA repair'
        }]
        actual = search.format_autocomplete_results(
            es_response,
            'go_name')
        self.assertEqual(actual, expected)
