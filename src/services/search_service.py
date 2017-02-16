from base_service import BaseService
from dao import ElasticSearchDAO

from helpers import *

class SearchService:

	def __init__(self):
		self.dao = ElasticSearchDAO()

	def autocomplete(self, query, category, field):
		if query == '':
			return { "results": None }

		return { "results": format_autocomplete_results(self.dao.search_by_body(build_autocomplete_search_body_request(query, category, field)), field) }

	def search(self, query, limit, offset, category, sort_by, params):
		# This needs to become a generic search object but for now this works
		category_filters = {
			"gene": ['gene_type', 'gene_biological_process', 'gene_molecular_function', 'gene_cellular_component', 'species'],
			"go": ['go_type', 'go_species', 'go_genes'],
			"disease": ['disease_species', 'disease_genes']
		}

		search_fields = ['id', 'name', 'symbol', 'synonyms', 'description', 'external_ids', 'species', 'gene_biological_process',
								'gene_molecular_function', 'gene_cellular_component', 'go_type', 'go_genes', 'go_synonyms', 'disease_genes',
								'disease_synonyms', 'homologs.symbol', 'homologs.panther_family']

		json_response_fields = ['name', 'symbol', 'synonyms', 'gene_type', 'gene_chromosomes','gene_chromosome_starts',
								'gene_chromosome_ends', 'description', 'external_ids', 'species', 'gene_biological_process',
								'gene_molecular_function', 'gene_cellular_component', 'go_type', 'go_genes', 'go_synonyms',
								'disease_genes', 'disease_synonyms', 'homologs', 'crossReferences', 'category', 'href']

		es_query = build_search_query(query, search_fields, category, category_filters, params)

		search_body = build_es_search_body_request(query, category, es_query, json_response_fields, search_fields, sort_by)

		search_results = self.dao.search_by_query(search_body, limit, offset, query)

		if search_results['hits']['total'] == 0:
			return { 'total': 0, 'results': [], 'aggregations': [] }

		aggregation_body = build_es_aggregation_body_request(es_query, category, category_filters)

		aggregation_results = self.dao.search_by_body(aggregation_body)

		return {
			'total': search_results['hits']['total'],
			'results': format_search_results(search_results, json_response_fields),
			'aggregations': format_aggregation_results( aggregation_results, category, category_filters)
		}

