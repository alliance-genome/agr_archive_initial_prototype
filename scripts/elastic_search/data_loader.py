from files import *
from loaders import *
from mods import *

import requests
import os
from elasticsearch import Elasticsearch

class DataLoader:
	gene_bkp_filename = "data/genes_bkp.pickle"
	go_bkp_filename = "data/go_bkp.pickle"
	so_bkp_filename = "data/so_bkp.pickle"
	diseases_bkp_filename = "data/diseases_bkp.pickle"

	def __init__(self):
		self.es = Elasticsearch(os.environ['ES_URI'], retry_on_timeout=True)

	def load_data_from_sources(self):
		#mods = [RGD(), MGI(), ZFIN(), SGD(), WormBase(), FlyBase()]
		mods = [MGI()]

		#go_data = GoLoader().get_data() 
		#omim_data = OMIMLoader().get_data()
		#so_data = SoLoader().get_data()

		genes = {}
		for mod in mods:
			genes.update(mod.load_genes())

		#HomoLogLoader(mods).attach_homolog_data(genes)

		#gene_go_annots = []
		#gene_disease_annots = []
		#for mod in mods:
		#	gene_go_annots.extend(mod.load_go())
		#	gene_disease_annots.extend(mod.load_diseases())

		#go_annot_loader = GoGeneAnnotLoader(genes, go_data)
		#go_entries = go_annot_loader.attach_annotations(gene_go_annots)

		#disease_annot_loader = DiseaseGeneAnnotLoader(genes, omim_data)
		#disease_entries = disease_annot_loader.attach_annotations(gene_disease_annots)
		
		PickleFile(self.gene_bkp_filename).save(genes)
		#PickleFile(self.go_bkp_filename).save(go_entries)
		#PickleFile(self.diseases_bkp_filename).save(disease_entries)
#		#PickleFile(self.so_bkp_filename).save(so)

	def load_data_from_files_into_index(self):
		self.delete_mapping()
		self.put_mapping()

		genes = PickleFile(self.gene_bkp_filename).load()
		go_entries = PickleFile(self.go_bkp_filename).load()
		disease_entries = PickleFile(self.diseases_bkp_filename).load()

		self.index_into_es(genes)
		self.index_into_es(go_entries)
		self.index_into_es(disease_entries)

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
	dataloader = DataLoader()
	#dataloader.load_data_from_files_into_index()
	dataloader.load_data_from_sources()
