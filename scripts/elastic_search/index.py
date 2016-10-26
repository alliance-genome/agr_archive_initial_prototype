from elasticsearch import Elasticsearch
import os
import requests

from mapping import mapping
from mod import MOD

INDEX_NAME = 'searchable_items_blue'
DOC_TYPE = 'searchable_item'
es = Elasticsearch(os.environ['ES_URI'], retry_on_timeout=True)


def delete_mapping():
    print "Deleting mapping..."
    response = requests.delete(os.environ['ES_URI'] + INDEX_NAME + "/")
    if response.status_code != 200:
        print "ERROR: " + str(response.json())
    else:
        print "SUCCESS"


def put_mapping():
    print "Putting mapping... "
    response = requests.put(os.environ['ES_URI'] + INDEX_NAME + "/", json=mapping)
    if response.status_code != 200:
        print "ERROR: " + str(response.json())
    else:
        print "SUCCESS"

genes = {}
go = {}
diseases = {}

species = ("M. musculus", "S. cerevisiae", "D. renio", "C. elegans", "D. melanogaster")

for specie in species:
    MOD.factory(specie).load_genes(genes)

for specie in species:
    MOD.factory(specie).load_diseases(genes, diseases)

for specie in species:
    MOD.factory(specie).load_go(genes, go)

delete_mapping()
put_mapping()

datatypes = [diseases, go, genes]

print "Indexing ElasticSearch..."

for datatype in datatypes:
    bulk_data = []

    for id in datatype:
        bulk_data.append({
            'index': {
                '_index': INDEX_NAME,
                '_type': DOC_TYPE,
                '_id': id
            }
        })
        bulk_data.append(datatype[id])

        if len(bulk_data) == 250:
            es.bulk(index=INDEX_NAME, body=bulk_data, refresh=True)
            bulk_data = []

    if len(bulk_data) > 0:
        es.bulk(index=INDEX_NAME, body=bulk_data, refresh=True)
