import os
import unittest
import mock
import json
from werkzeug.datastructures import ImmutableMultiDict

from src import search


class SearchEndpointsTest(unittest.TestCase):

    def setUp(self):
        os.environ['ES_URI'] = 'http://localhost:9200/'
        from src.server import app

        self.es_search_response = {
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
                "hits": [{
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
                }]
            }
        }

        self.es_aggregation_response = {
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
        self.index = 'searchable_items_prototype'
        self.search_fields = [
            'name',
            'symbol',
            'synonym',
            'go_ids',
            'go_names'
        ]
        self.json_response_fields = [
            'name',
            'symbol',
            'synonym',
            'go_ids',
            'go_names',
            'href',
            'type',
            'organism'
        ]
        self.category_filters = {
            "gene": ['go_ids', 'go_names'],
            "go": ['gene']
        }
        self.app = app.test_client()
        self.app.testing = True

    @mock.patch('src.server.es.search')
    def test_search_default_params(self, mock_es):
        def side_effect(*args, **kwargs):
            if "size" in kwargs:
                return self.es_search_response
            else:
                return self.es_aggregation_response

        mock_es.side_effect = side_effect

        response = self.app.get('/api/search')

        es_query = search.build_search_query(
            '',
            self.search_fields,
            '',
            self.category_filters,
            {}
        )

        mock_es.assert_has_calls([mock.call(
            index=self.index,
            body=search.build_es_search_body_request(
                '',
                '',
                es_query,
                self.json_response_fields,
                self.search_fields,
                ''
            ),
            size=10,
            from_=0
        )])

        mock_es.assert_has_calls([mock.call(
            index=self.index,
            body=search.build_es_aggregation_body_request(
                es_query,
                '',
                self.category_filters
            )
        )])

        self.assertEqual(response.status_code, 200)

    @mock.patch('src.server.es.search')
    def test_search_with_custom_params(self, mock_es):
        def side_effect(*args, **kwargs):
            if "size" in kwargs:
                return self.es_search_response
            else:
                return self.es_aggregation_response

        mock_es.side_effect = side_effect

        response = self.app.get(
            ('/api/search?'
             'q=act1&'
             'category=gene&'
             'limit=25&'
             'offset=10&'
             'sort_by=alphabetical')
        )

        es_query = search.build_search_query(
            "act1",
            self.search_fields,
            "gene",
            self.category_filters,
            ImmutableMultiDict([
                ("q", "act1"),
                ("category", "gene"),
                ("limit", 25),
                ("offset", 10),
                ("sort_by", "alphabetical")
            ])
        )

        mock_es.assert_has_calls([mock.call(
            index=self.index,
            body=search.build_es_search_body_request(
                "act1",
                "gene",
                es_query,
                self.json_response_fields,
                self.search_fields,
                "alphabetical"
            ),
            size=25,
            from_=10
        )])

        mock_es.assert_has_calls([mock.call(
            index=self.index,
            body=search.build_es_aggregation_body_request(
                es_query,
                "gene",
                self.category_filters
            )
        )])

        self.assertEqual(response.status_code, 200)

    @mock.patch('src.server.es.search')
    def test_search_with_aggregation_params(self, mock_es):
        def side_effect(*args, **kwargs):
            if "size" in kwargs:
                return self.es_search_response
            else:
                return self.es_aggregation_response

        mock_es.side_effect = side_effect

        response = self.app.get(
            ('/api/search?'
             'q=act1&'
             'category=gene&'
             'go_names=cytoplasm')
        )

        es_query = search.build_search_query(
            "act1",
            self.search_fields,
            "gene",
            self.category_filters,
            ImmutableMultiDict([
                ("q", "act1"),
                ("category", "gene"),
                ("go_names", "cytoplasm")
            ])
        )

        mock_es.assert_has_calls([mock.call(
            index=self.index,
            body=search.build_es_search_body_request(
                "act1",
                "gene",
                es_query,
                self.json_response_fields,
                self.search_fields,
                ""
            ),
            size=10,
            from_=0
        )])

        mock_es.assert_has_calls([mock.call(
            index=self.index,
            body=search.build_es_aggregation_body_request(
                es_query,
                "gene",
                self.category_filters
            )
        )])

        self.assertEqual(response.status_code, 200)

    @mock.patch('src.server.es.search')
    def test_empty_search_returns_json_object(self, mock_es):
        def side_effect(*args, **kwargs):
            if "size" in kwargs:
                self.es_search_response['hits']['total'] = 0
                return self.es_search_response
            else:
                return self.es_aggregation_response

        mock_es.side_effect = side_effect

        response = self.app.get((
            '/api/search?'
            'q=act1&'
            'category=gene&'
            'go_names=cytoplasm'))

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)

        self.assertEqual(data, {
            'total': 0,
            'results': [],
            'aggregations': []
        })

    @mock.patch('src.server.es.search')
    def test_search_returns_json_object(self, mock_es):
        def side_effect(*args, **kwargs):
            if "size" in kwargs:
                return self.es_search_response
            else:
                return self.es_aggregation_response

        mock_es.side_effect = side_effect

        response = self.app.get(
            ('/api/search?'
             'q=act1&'
             'category=gene&'
             'go_names=cytoplasm')
        )

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data, {
            'total': self.es_search_response['hits']['total'],
            'results': search.format_search_results(
                self.es_search_response,
                self.json_response_fields
            ),
            'aggregations': search.format_aggregation_results(
                self.es_aggregation_response,
                'gene',
                self.category_filters
            )
        })

    @mock.patch('src.server.es.search')
    def test_search_autocomplete_es_params(self, mock_es):
        mock_es.return_value = self.es_search_response

        self.app.get('/api/search_autocomplete?q=act')

        mock_es.assert_called_with(
            index=self.index,
            body=search.build_autocomplete_search_body_request(
                'act',
                '',
                'name')
        )

        self.app.get('/api/search_autocomplete?q=act&category=go')

        mock_es.assert_called_with(
            index=self.index,
            body=search.build_autocomplete_search_body_request(
                'act',
                'go',
                'name')
        )

        mock_es.return_value = {
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

        self.app.get(
            ('/api/search_autocomplete?'
             'q=act&'
             'category=go&'
             'field=go_name')
        )
        mock_es.assert_called_with(
            index=self.index,
            body=search.build_autocomplete_search_body_request(
                'act',
                'go',
                'go_name')
        )

    @mock.patch('src.server.es.search')
    def test_search_autocomplete_returns_object(self, mock_es):
        mock_es.return_value = self.es_search_response

        response = self.app.get('/api/search_autocomplete?q=act')

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        results = search.format_autocomplete_results(self.es_search_response)
        expected = dict(results=results)
        self.assertEqual(data, expected)

    def test_search_autocomplete_returns_none_for_empty_query(self):
        response = self.app.get('/api/search_autocomplete')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {
            'results': None
        })

        response = self.app.get('/api/search_autocomplete?q=')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {
            'results': None
        })
