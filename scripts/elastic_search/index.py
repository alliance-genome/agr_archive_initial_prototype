from elasticsearch import Elasticsearch
from intermine.webservice import Service

from mapping import mapping
import os
import requests
import pickle
import time

INDEX_NAME = 'searchable_items_prototype'
DOC_TYPE = 'searchable_item'
ES_ADDRESS = os.environ['ES_URI']
es = Elasticsearch(ES_ADDRESS, retry_on_timeout=True)

def delete_mapping():
    print "Deleting mapping..."
    response = requests.delete(ES_ADDRESS + INDEX_NAME + "/")
    if response.status_code != 200:
        print "ERROR: " + str(response.json())
    else:
        print "SUCCESS"        

def put_mapping():
    print "Putting mapping... "
    response = requests.put(ES_ADDRESS + INDEX_NAME + "/", json=mapping)
    if response.status_code != 200:
        print "ERROR: " + str(response.json())
    else:
        print "SUCCESS"

backup_filename = "yeastmine_genes_" + time.strftime("%m_%d_%Y") + ".bkp"
if os.path.isfile(backup_filename):
    print "Restoring old fetched data from Yeastmine"

    backup = open(backup_filename, 'rb')
    yeast_genes = pickle.load(backup)
else:
    print "Fetching data from YeastMine"
    service = Service("http://yeastmine.yeastgenome.org/yeastmine/service")

    query = service.new_query("Gene")
    query.add_view(
        "primaryIdentifier", "secondaryIdentifier", "symbol", "name",
        "goAnnotation.ontologyTerm.identifier", "goAnnotation.ontologyTerm.name"
    )
    query.add_constraint("organism.name", "=", "Saccharomyces cerevisiae", code = "B")

    rows = query.rows()

    yeast_genes = {}

    for row in rows:
        id = row["primaryIdentifier"]
    
        if id in yeast_genes:
            yeast_genes[id]["go_ids"].append(row["goAnnotation.ontologyTerm.identifier"])
            yeast_genes[id]["go_names"].append(row["goAnnotation.ontologyTerm.name"])
        else:
            yeast_genes[id] = {
                "name": row["name"],
                "symbol": row["symbol"],
                "synonym": row["secondaryIdentifier"],
                "go_ids": [row["goAnnotation.ontologyTerm.identifier"]],
                "go_names": [row["goAnnotation.ontologyTerm.name"]],
                "href": "http://www.yeastgenome.org/" + row["primaryIdentifier"] + "/overview",
                "type": "gene"
            }

    with open(backup_filename, 'wb') as backup:
        pickle.dump(yeast_genes, backup)

print "Indexing " + str(len(yeast_genes)) + " yeast genes"

bulk_data = []
for gene in yeast_genes.keys():
    bulk_data.append({
        'index': {
            '_index': INDEX_NAME,
            '_type': DOC_TYPE,
            '_id': "yeast_" + gene
        }
    })
    bulk_data.append(yeast_genes[gene])

    if len(bulk_data) % 500 == 0:
        es.bulk(index=INDEX_NAME, body=bulk_data, refresh=True)
        bulk_data = []

if len(bulk_data) > 0:
    es.bulk(index=INDEX_NAME, body=bulk_data, refresh=True)
