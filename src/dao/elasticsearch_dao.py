import os

from elasticsearch import Elasticsearch

class ElasticSearchDAO(object):

    def __init__(self, app):
        self.index = app.config['ES_INDEX']
        if app.config['ES_AWS']:
            self.es = Elasticsearch(app.config['ES_URI'], timeout=30, retry_on_timeout=False, use_ssl=True, verify_certs=True)
        else:
            self.es = Elasticsearch(app.config['ES_URI'], timeout=30, retry_on_timeout=False)

    def get_by_id(self, id):
        return self.es.get(self.index, id)

    def search_by_body(self, body_request):
        return self.es.search(index=self.index, body=body_request)

    def search_by_query(self, body_request, limit, offset, query):
        return self.es.search(index=self.index, body=body_request, size=limit, from_=offset, preference='p_' + query)
