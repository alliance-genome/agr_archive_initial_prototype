import unittest
from src.search import build_search_query, build_search_params, build_es_search_body_request


class SearchHelpersTest(unittest.TestCase):
    def test_build_search_params_should_search_for_all_with_empty_query(self):
        query = ""
        fields = ["name", "symbol"]

        self.assertEqual(build_search_params(query, fields), {
            "match_all": {}
        })

    def test_build_search_params_should_create_general_query(self):
        query = "gene"
        fields = ["name", "symbol"]

        self.assertEqual(build_search_params(query, fields), {
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
            }
        })

    def test_build_search_params_should_quote_queries_with_special_chars(self):
        query = "eu-gene"
        fields = ["name", "symbol"]

        self.assertEqual(build_search_params(query, fields), {
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

    def test_build_search_params_should_treated_quoted_query(self):
        query = '"gene"'
        fields = ["name", "symbol"]

        self.assertEqual(build_search_params(query, fields), {
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

    def test_build_search_query_should_return_search_params_only_for_no_category(self):
        query = "gene"
        fields = ["name", "symbol"]
        category = ''
        category_filters =  {
            "genes": ['go_ids', 'go_names'],
            "go": ['gene'],
        }
        args = {}

        es_query = build_search_params(query, fields)

        self.assertEqual(build_search_query(query, fields, category, category_filters, args), es_query)

    def test_build_search_query_should_filter_by_category(self):
        query = "gene"
        fields = ["name", "symbol"]
        category = 'genes'
        category_filters =  {
            "genes": ['go_ids', 'go_names'],
            "go": ['gene'],
        }
        args = {}

        es_query = build_search_params(query, fields)

        self.assertEqual(build_search_query(query, fields, category, category_filters, args), {
            'filtered': {
                'query': es_query,
                'filter': {
                    'bool': {
                        'must': [{'term': {'category': category}}]
                    }
                }
            }
        })

    def test_build_search_query_should_filter_subcategories_if_passed(self):
        query = "act1"
        fields = ["name", "symbol"]
        category = "genes"
        category_filters =  {
            "genes": ['go_ids', 'go_names'],
            "go": ['gene'],
        }
        args = {'go_names': 'A,B,C'}

        es_query = build_search_params(query, fields)

        self.assertEqual(build_search_query(query, fields, category, category_filters, args), {
            'filtered': {
                'query': es_query,
                'filter': {
                    'bool': {
                        'must': [{'term': {'category': category}}, {'term': {'go_names.raw': 'A,B,C'}}]
                    }
                }
            }
        })

    def test_build_es_search_body_should_randomize_results_if_empty_query_and_empty_category(self):
        query = ""
        fields = ["name", "symbol"]
        category = ""
        category_filters = {
            "genes": ['go_ids', 'go_names'],
            "go": ['gene'],
        }
        sort_by = "relevance"
        args = {'go_names': 'A,B,C'}
        search_fields = []
        json_response_fields = ['name', 'symbol', 'synonym']

        es_query = build_search_query(query, fields, category, category_filters, args)

        self.assertEqual(build_es_search_body_request(query, category, es_query, json_response_fields, search_fields, sort_by), {
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
        })

    def test_build_es_search_body_should_add_highlighting(self):
        query = ""
        fields = ["name", "symbol"]
        category = ""
        category_filters = {
            "genes": ['go_ids', 'go_names'],
            "go": ['gene'],
        }
        sort_by = "relevance"
        args = {'go_names': 'A,B,C'}
        search_fields = ["name", "symbol"]
        json_response_fields = ['name', 'symbol', 'synonym']

        es_query = build_search_query(query, fields, category, category_filters, args)

        self.assertEqual(build_es_search_body_request(query, category, es_query, json_response_fields, search_fields, sort_by), {
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
        })

    def test_build_es_search_body_should_sort_alphabetically_by_name(self):
        query = ""
        fields = ["name", "symbol"]
        category = ""
        category_filters = {
            "genes": ['go_ids', 'go_names'],
            "go": ['gene'],
        }
        sort_by = "alphabetical"
        args = {'go_names': 'A,B,C'}
        search_fields = ["name", "symbol"]
        json_response_fields = ['name', 'symbol', 'synonym']

        es_query = build_search_query(query, fields, category, category_filters, args)

        self.assertEqual(build_es_search_body_request(query, category, es_query, json_response_fields, search_fields, sort_by), {
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
        })

    def test_build_es_search_body_should_not_randomize_results_if_category_is_defined(self):
        query = ""
        fields = ["name", "symbol"]
        category = "genes"
        category_filters = {
            "genes": ['go_ids', 'go_names'],
            "go": ['gene'],
        }
        sort_by = "alphabetical"
        args = {'go_names': 'A,B,C'}
        search_fields = ["name", "symbol"]
        json_response_fields = ['name', 'symbol', 'synonym']

        es_query = build_search_query(query, fields, category, category_filters, args)

        self.assertEqual(build_es_search_body_request(query, category, es_query, json_response_fields, search_fields, sort_by), {
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
        })
