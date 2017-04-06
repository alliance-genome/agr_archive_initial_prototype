import os
import unittest
import mock
import json
from werkzeug.datastructures import ImmutableMultiDict

os.environ['ES_HOST'] = 'localhost:9200'
os.environ['ES_INDEX'] = 'searchable_items_blue'
os.environ['ES_AWS'] = 'false'

from services.helpers import *
from server import app

class SearchEndpointsTest(unittest.TestCase):
    def setUp(self):

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
        self.index = os.environ['ES_INDEX']
        self.search_fields = ['primaryId', 'name', 'symbol', 'symbol.raw', 'synonyms', 'synonyms.raw', 'description',
                              'external_ids', 'species', 'gene_biological_process', 'gene_molecular_function',
                              'gene_cellular_component', 'go_type', 'go_genes', 'go_synonyms', 'disease_genes',
                              'disease_synonyms']
        self.json_response_fields = ['name', 'symbol', 'synonyms', 'soTermName', 'gene_chromosomes','gene_chromosome_starts', 'gene_chromosome_ends', 'description', 'external_ids', 'species', 'gene_biological_process', 'gene_molecular_function', 'gene_cellular_component', 'go_type', 'go_genes', 'go_synonyms', 'disease_genes', 'disease_synonyms', 'homologs', 'crossReferences', 'category', 'href']
        self.category_filters = {
            "gene": ['soTermName', 'gene_biological_process', 'gene_molecular_function', 'gene_cellular_component', 'species'],
            "go": ['go_type', 'go_species', 'go_genes'],
            "disease": ['disease_species', 'disease_genes']
        }

        self.app = app.test_client()
        self.app.testing = True

    @mock.patch('server.es.search')
    def test_mock_es(self, mock_es):
        mock_es.return_value = self.es_search_response
        self.app.get('/api/search_autocomplete?q=act')
        mock_es.assert_called()

    @mock.patch('server.es.search')
    def test_search_default_params(self, mock_es):
        def side_effect(*args, **kwargs):
            if "size" in kwargs:
                return self.es_search_response
            else:
                return self.es_aggregation_response

        mock_es.side_effect = side_effect

        response = self.app.get('/api/search')

        es_query = build_search_query(
            '',
            self.search_fields,
            '',
            self.category_filters,
            {}
        )

        mock_es.assert_has_calls([mock.call(
            index=self.index,
            body=build_es_search_body_request(
                '',
                '',
                es_query,
                self.json_response_fields,
                self.search_fields,
                ''
            ),
            size=10,
            from_=0,
            preference='p_'
        )])

        mock_es.assert_has_calls([mock.call(
            index=self.index,
            body=build_es_aggregation_body_request(
                es_query,
                '',
                self.category_filters
            )
        )])

        self.assertEqual(response.status_code, 200)

    @mock.patch('server.es.search')
    def test_search_with_custom_params(self, mock_es):
        def side_effect(*args, **kwargs):
            if "size" in kwargs:
                return self.es_search_response
            else:
                return self.es_aggregation_response

        mock_es.side_effect = side_effect

        response = self.app.get('/api/search?q=act1&category=gene&limit=25&offset=10&sort_by=alphabetical')

        es_query = build_search_query(
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
            body=build_es_search_body_request(
                "act1",
                "gene",
                es_query,
                self.json_response_fields,
                self.search_fields,
                "alphabetical"
            ),
            size=25,
            from_=10,
            preference='p_act1'
        )])

        mock_es.assert_has_calls([mock.call(
            index=self.index,
            body=build_es_aggregation_body_request(
                es_query,
                "gene",
                self.category_filters
            )
        )])

        self.assertEqual(response.status_code, 200)

    @mock.patch('server.es.search')
    def test_search_with_aggregation_params(self, mock_es):
        def side_effect(*args, **kwargs):
            if "size" in kwargs:
                return self.es_search_response
            else:
                return self.es_aggregation_response

        mock_es.side_effect = side_effect

        response = self.app.get('/api/search?q=act1&category=gene&go_names=cytoplasm')

        es_query = build_search_query(
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
            body=build_es_search_body_request(
                "act1",
                "gene",
                es_query,
                self.json_response_fields,
                self.search_fields,
                ""
            ),
            size=10,
            from_=0,
            preference='p_act1'
        )])

        mock_es.assert_has_calls([mock.call(
            index=self.index,
            body=build_es_aggregation_body_request(
                es_query,
                "gene",
                self.category_filters
            )
        )])

        self.assertEqual(response.status_code, 200)

    @mock.patch('server.es.search')
    def test_empty_search_returns_json_object(self, mock_es):
        def side_effect(*args, **kwargs):
            if "size" in kwargs:
                self.es_search_response['hits']['total'] = 0
                return self.es_search_response
            else:
                return self.es_aggregation_response

        mock_es.side_effect = side_effect

        response = self.app.get('/api/search?q=thisisntgoingtomatchanything&category=gene&go_names=thiswontmatcheither')

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)

        self.assertEqual(data, {
            'total': 0,
            'results': [],
            'aggregations': []
        })

    @mock.patch('server.es.search')
    def test_search_returns_json_object(self, mock_es):
        def side_effect(*args, **kwargs):
            if "size" in kwargs:
                return self.es_search_response
            else:
                return self.es_aggregation_response

        mock_es.side_effect = side_effect

        response = self.app.get('/api/search?q=act1&category=gene&go_names=cytoplasm')

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)

    @mock.patch('server.es.search')
    def test_search_autocomplete_es_params(self, mock_es):
        mock_es.return_value = self.es_search_response

        self.app.get('/api/search_autocomplete?q=act')

        mock_es.assert_called_with(
            index=self.index,
            body=build_autocomplete_search_body_request('act', '', 'name_key')
        )

        self.app.get('/api/search_autocomplete?q=act&category=go')

        mock_es.assert_called_with(
            index=self.index,
            body=build_autocomplete_search_body_request('act', 'go', 'name_key')
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

        self.app.get('/api/search_autocomplete?q=act&category=go&field=go_name')

        mock_es.assert_called_with(
            index=self.index,
            body=build_autocomplete_search_body_request('act', 'go', 'go_name')
        )

    @mock.patch('server.es.search')
    def test_search_autocomplete_returns_object(self, mock_es):
        mock_es.return_value = self.es_search_response

        response = self.app.get('/api/search_autocomplete?q=act')

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data, {
            'results': format_autocomplete_results(self.es_search_response)
        })

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
