from files import *
from loaders import *
from mods import *

import requests
import os
from elasticsearch import Elasticsearch

class LoadAndIndex:
	gene_bkp_filename = "data/genes_bkp.pickle"
	go_bkp_filename = "data/go_bkp.pickle"
	so_bkp_filename = "data/so_bkp.pickle"
	diseases_bkp_filename = "data/diseases_bkp.pickle"

	def __init__(self):
		if os.environ['ES_AWS'] == "true":
			self.es = Elasticsearch(os.environ['ES_URI'], timeout=5, retry_on_timeout=False, use_ssl=True, verify_certs=True)
		else:
			self.es = Elasticsearch(os.environ['ES_URI'], timeout=5, retry_on_timeout=False)

	def load_data_from_files_into_index(self):
		print "Load data from saved files"
		genes = PickleFile(self.gene_bkp_filename).load()
		go_entries = PickleFile(self.go_bkp_filename).load()
		# disease_entries = PickleFile(self.diseases_bkp_filename).load()

		print "Delete and Recreate Index"
		self.delete_mapping()
		self.put_mapping()

		print "Send data into Index"
		self.index_into_es(genes)
		self.index_into_es(go_entries)
		# self.index_into_es(disease_entries)

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
	load_and_index = LoadAndIndex()
	load_and_index.load_data_from_files_into_index()
