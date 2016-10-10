from __future__ import print_function
import os
import pickle
import requests
import time

from elasticsearch import Elasticsearch
from intermine.webservice import Service

from mapping import mapping

INDEX_NAME = 'searchable_items_prototype'
DOC_TYPE = 'searchable_item'
es = Elasticsearch(os.environ['ES_URI'], retry_on_timeout=True)


def delete_mapping():
    print("Deleting mapping...")
    response = requests.delete(os.environ['ES_URI'] + INDEX_NAME + "/")
    if response.status_code != 200:
        print("ERROR: " + str(response.json()))
    else:
        print("SUCCESS")


def put_mapping():
    print("Putting mapping... ")
    response = requests.put(os.environ['ES_URI'] + INDEX_NAME + '/', json=mapping)
    if response.status_code != 200:
        print("ERROR: " + str(response.json()))
    else:
        print("SUCCESS")


def index_genes(organism, mod):
    backup_filename = organism + "mine_genes_" + time.strftime("%m_%d_%Y") + ".bkp"
    if os.path.isfile(backup_filename):
        print("Restoring fetched data from today from " + organism + "mine")
        backup = open(backup_filename, 'rb')
        genes = pickle.load(backup)
    else:
        print("Fetching data from " + organism + "mine")
        service = Service(mod["mine_service_url"])
        query = service.new_query("Gene")
        query.add_view(mod["gene_fields"].values())
        query.add_constraint("organism.name", "=", mod["mine_organism_name"], code="B")
        rows = query.rows()
        genes = {}
        for row in rows:
            id = row[mod["gene_fields"]["id"]]
            if id in genes:
                genes[id]["go_ids"].append(row[mod["gene_fields"]["go_id"]])
                genes[id]["go_names"].append(row[mod["gene_fields"]["go_name"]])
            else:
                genes[id] = {
                    "name": row[mod["gene_fields"]["gene_name"]],
                    "symbol": row[mod["gene_fields"]["gene_symbol"]],
                    "synonym": row[mod["gene_fields"]["gene_synonym"]],
                    "go_ids": [row[mod["gene_fields"]["go_id"]]],
                    "go_names": [row[mod["gene_fields"]["go_name"]]],
                    "href": mod["url_prefix"] + row["primaryIdentifier"] + mod["url_suffix"],
                    "organism": organism,
                    "category": "gene"
                }
        with open(backup_filename, 'wb') as backup:
            pickle.dump(genes, backup)

    print("Indexing " + str(len(genes)) + " " + organism + " genes")
    bulk_data = []
    for gene in genes.keys():
        bulk_data.append({
            'index': {
                '_index': INDEX_NAME,
                '_type': DOC_TYPE,
                '_id': organism + "_" + gene
            }
        })
        bulk_data.append(genes[gene])

        if len(bulk_data) % 500 == 0:
            es.bulk(index=INDEX_NAME, body=bulk_data, refresh=True)
            bulk_data = []

    if len(bulk_data) > 0:
        es.bulk(index=INDEX_NAME, body=bulk_data, refresh=True)


delete_mapping()
put_mapping()

mods = {
    "yeast": {
        "mine_service_url": "http://yeastmine.yeastgenome.org/yeastmine/service",
        "mine_organism_name": "Saccharomyces cerevisiae",
        "gene_fields": {
            "id": "primaryIdentifier",
            "go_id": "goAnnotation.ontologyTerm.identifier",
            "go_name": "goAnnotation.ontologyTerm.name",
            "gene_name": "name",
            "gene_symbol": "symbol",
            "gene_synonym": "secondaryIdentifier"
        },
        "url_prefix": "http://www.yeastgenome.org/locus/",
        "url_suffix": "/overview"
    }
}

for organism in mods:
    index_genes(organism, mods[organism])
