import os

from elasticsearch import Elasticsearch

class ElasticSearchDAO:
	ES_INDEX = os.environ['ES_INDEX']
	if os.environ['ES_AWS'] == "true":
		es = elasticsearch(os.environ['ES_URI'], timeout=5, retry_on_timeout=false, use_ssl=true, verify_certs=true)
	else:
		es = elasticsearch(os.environ['ES_URI'], timeout=5, retry_on_timeout=false)

	def __init__(self):
		pass

	def get_by_id(self, id):
		return ElasticSearchDAO.es.get(ElasticSearchDAO.ES_INDEX, id)

	def search_by_body(self, body_request):
		return ElasticSearchDAO.es.search(index=ElasticSearchDAO.ES_INDEX, body=body_request)

	def search_by_query(self, body_request, limit, offset, query):
		return ElasticSearchDAO.es.search(index=ElasticSearchDAO.ES_INDEX, body=body_request, size=limit, from_=offset, preference='p_'+query)
