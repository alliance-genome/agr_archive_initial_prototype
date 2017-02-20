from files import *
from loaders import *
from mods import *

import requests
import os
from elasticsearch import Elasticsearch

class FetchSaveIndex:
	gene_bkp_filename = "data/genes_bkp.pickle"
	go_bkp_filename = "data/go_bkp.pickle"
	so_bkp_filename = "data/so_bkp.pickle"
	diseases_bkp_filename = "data/diseases_bkp.pickle"

	def __init__(self):
		if os.environ['ES_AWS'] == "true":
			self.es = Elasticsearch(os.environ['ES_URI'], timeout=5, retry_on_timeout=False, use_ssl=True, verify_certs=True)
		else:
			self.es = Elasticsearch(os.environ['ES_URI'], timeout=5, retry_on_timeout=False)

	def load_data_from_sources_and_index(self):
		mods = [RGD(), MGI(), ZFIN(), SGD(), WormBase(), FlyBase()]

		print "Loading Go Data"
		go_data = GoLoader().get_data() 
		print "Loading OMIM Data"
		omim_data = OMIMLoader().get_data()
		print "Loading SO Data"
		so_loader = SoLoader()

		genes = {}
		print "Gathering genes from Each Mod"
		for mod in mods:
			genes.update(mod.load_genes())

		print "Loading Homologs for all genes"
		HomoLogLoader(mods).attach_homolog_data(genes)
		print "Loading SO terms for all genes"
		so_loader.attach_so_data(genes)

		print "Loading Go and Disease annotations for genes from mines"
		gene_go_annots = []
		gene_disease_annots = []
		for mod in mods:
			gene_go_annots.extend(mod.load_go())
			gene_disease_annots.extend(mod.load_diseases())

		print "Attaching GO annotations to genes"
		go_annot_loader = GoGeneAnnotLoader(genes, go_data)
		go_entries = go_annot_loader.attach_annotations(gene_go_annots)

		print "Attaching Disease annotations to genes"
		disease_annot_loader = DiseaseGeneAnnotLoader(genes, omim_data)
		disease_entries = disease_annot_loader.attach_annotations(gene_disease_annots)

		print "Delete and Recreate Index"
		self.delete_mapping()
		self.put_mapping()

		print "Send data into Index"
		self.index_into_es(genes)
		self.index_into_es(go_entries)
		self.index_into_es(disease_entries)

		print "Saving processed data to files"
		PickleFile(self.gene_bkp_filename).save(genes)
		PickleFile(self.go_bkp_filename).save(go_entries)
		PickleFile(self.diseases_bkp_filename).save(disease_entries)
		PickleFile(self.so_bkp_filename).save(so_loader.get_data())

	def delete_mapping(self):
		print "Deleting mapping..."
		response = requests.delete(os.environ['ES_URI'] + os.environ['ES_INDEX'] + "/")
		if response.status_code != 200:
			print "ERROR: " + str(response.json())
		else:
			print "SUCCESS"

	def put_mapping(self):
		from mapping import mapping

		print "Putting mapping... "
		response = requests.put(os.environ['ES_URI'] + os.environ['ES_INDEX'] + "/", json=mapping)
		if response.status_code != 200:
			print "ERROR: " + str(response.json())
		else:
			print "SUCCESS"

	def index_into_es(self, data):
		bulk_data = []

		for id in data:
			bulk_data.append({
				'index': {
					'_index': os.environ['ES_INDEX'], 
					'_type': "searchable_item",
					'_id': id
				}
			})
			bulk_data.append(data[id])

			if len(bulk_data) == 300:
				self.es.bulk(index=os.environ['ES_INDEX'], body=bulk_data, refresh=True)
				bulk_data = []

		if len(bulk_data) > 0:
			self.es.bulk(index=os.environ['ES_INDEX'], body=bulk_data, refresh=True)

if __name__ == '__main__':
	fetch_save_index = FetchSaveIndex()
	fetch_save_index.load_data_from_sources_and_index()
