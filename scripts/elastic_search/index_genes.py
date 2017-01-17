import os
from elasticsearch import Elasticsearch

GENES_INDEX_NAME = 'agr_gene'
GENES_INDEX_DOC_TYPE = GENES_INDEX_NAME

def index_genes():
    es = Elasticsearch(os.environ['ES_URI'], retry_on_timeout=True)

    # create index, only do this the first time
    # es.indices.create(index=GENES_INDEX_NAME, ignore=400)
    # save example data
    example_body = {
        "id": 123,
        "name": "GENE123",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    }
    es.index(index=GENES_INDEX_NAME, doc_type=GENES_INDEX_DOC_TYPE, id=123, body=example_body)

    # how to retrieve later
    # es.get(index=GENES_INDEX_NAME, doc_type=GENES_INDEX_DOC_TYPE, id=123)['_source']

index_genes()
