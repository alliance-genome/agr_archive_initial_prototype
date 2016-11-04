from elasticsearch import Elasticsearch
import os
import requests
import pickle

import time

from mapping import mapping

from sgd import SGD
from zfin import ZFin
from worm import WormBase
from fly import FlyBase
from mouse import MGI
from rat import RGD

from mod import MOD

sgd = SGD()
zfin = ZFin()
worm = WormBase()
fly = FlyBase()
mouse = MGI()
rat = RGD()

mod = MOD()

mods = [mouse, zfin, sgd, worm, fly, rat]

for m in mods:
    start_time = time.time()
    m.load_genes()
    print (" --- %s seconds --- " % (time.time() - start_time))

mod.load_homologs()

for m in mods:
    start_time = time.time()
    m.load_go()
    print (" --- %s seconds --- " % (time.time() - start_time))

for m in mods:
    start_time = time.time()
    m.load_diseases()
    print (" --- %s seconds --- " % (time.time() - start_time))

mod.save_into_file()

mod.delete_mapping()
mod.put_mapping()

mod.index_genes_into_es()
mod.index_go_into_es()
mod.index_diseases_into_es()

import pdb; pdb.set_trace()



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
homology = {}

species = ["M. musculus", "S. cerevisiae", "D. rerio", "C. elegans", "D. melanogaster"]


#go_dataset = MOD().load_go()
#import pdb; pdb.set_trace()

mod = MOD()

if os.path.isfile(gene_bkp_filename):
    with open(gene_bkp_filename, "rb") as f:
        print "Loading all gene data from backup file..."
        mod.genes = pickle.load(f)
else:
    for s in species:
        MOD.factory(s).load_genes(mod.genes)

MOD.load_homologs(mod.genes)

if os.path.isfile(go_bkp_filename):
    with open(go_bkp_filename, "rb") as f:
        print "Loading all go data from backup file..."
        go = pickle.load(f)
else:
    for s in species:
        MOD.factory(s).load_go(genes, go)

if os.path.isfile(diseases_bkp_filename):
    with open(diseases_bkp_filename, "rb") as f:
        print "Loading all diseases data from backup file..."
        diseases = pickle.load(f)
else:
    for s in species:
        MOD.factory(s).load_diseases(genes, diseases)

#delete_mapping()
#put_mapping()

#datatypes = [genes, diseases, go]
datatypes = [genes]

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


if not os.path.isfile(gene_bkp_filename):
    with open(gene_bkp_filename, "wb") as f:
        print "Saving gene data into a backup file..."
        pickle.dump(genes, f, pickle.HIGHEST_PROTOCOL)

if not os.path.isfile(go_bkp_filename):
    with open(go_bkp_filename, "wb") as f:
        print "Saving go data into a backup file..."
        pickle.dump(go, f, pickle.HIGHEST_PROTOCOL)

if not os.path.isfile(diseases_bkp_filename):
    with open(diseases_bkp_filename, "wb") as f:
        print "Saving diseases data into a backup file..."
        pickle.dump(diseases, f, pickle.HIGHEST_PROTOCOL)
