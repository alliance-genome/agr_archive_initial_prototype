from files import *
from loaders import *
from mods import *

class DataLoader:
	gene_bkp_filename = "data/genes_bkp.pickle"
	go_bkp_filename = "data/go_bkp.pickle"
	so_bkp_filename = "data/so_bkp.pickle"
	diseases_bkp_filename = "data/diseases_bkp.pickle"

	def load_data(self):
		mods = [MGI(), ZFIN(), SGD(), WormBase(), FlyBase(), RGD()]
		#mods = [MGI()]

		go_data = GoLoader().get_data() 
		omim_data = OMIMLoader().get_data()
		#so_data = SoLoader().get_data()

		genes = {}
		for mod in mods:
			genes.update(mod.load_genes())

		HomoLogLoader(mods).attach_homolog_data(genes)

		gene_go_annots = []
		gene_disease_annots = []
		for mod in mods:
			gene_go_annots.extend(mod.load_go())
			gene_disease_annots.extend(mod.load_diseases())

		go_annot_loader = GoGeneAnnotLoader(genes, go_data)
		go_entries = go_annot_loader.attach_annotations(gene_go_annots)

		disease_annot_loader = DiseaseGeneAnnotLoader(genes, omim_data)
		disease_entries = disease_annot_loader.attach_annotations(gene_disease_annots)
		
		PickleFile(self.gene_bkp_filename).save(genes)
		PickleFile(self.go_bkp_filename).save(go_entries)
		PickleFile(self.diseases_bkp_filename).save(disease_entries)
#		#PickleFile(self.so_bkp_filename).save(so)
#
#
#
#	def delete_mapping(self):
#		print "Deleting mapping..."
#		response = requests.delete(os.environ['ES_URI'] + self.INDEX_NAME + "/")
#		if response.status_code != 200:
#			print "ERROR: " + str(response.json())
#		else:
#			print "SUCCESS"
#
#	def put_mapping(self):
#		from mapping import mapping
#
#		print "Putting mapping... "
#		response = requests.put(os.environ['ES_URI'] + self.INDEX_NAME + "/", json=mapping)
#		if response.status_code != 200:
#			print "ERROR: " + str(response.json())
#		else:
#			print "SUCCESS"
#
#	def index_into_es(self, data):
#		bulk_data = []
#
#		for id in data:
#			bulk_data.append({
#				'index': {
#					'_index': self.INDEX_NAME,
#					'_type': self.DOC_TYPE,
#					'_id': id
#				}
#			})
#			bulk_data.append(data[id])
#
#			if len(bulk_data) == 300:
#				self.es.bulk(index=self.INDEX_NAME, body=bulk_data, refresh=True)
#				bulk_data = []
#
#		if len(bulk_data) > 0:
#			self.es.bulk(index=self.INDEX_NAME, body=bulk_data, refresh=True)
#
#		#mod.index_genes_into_es()
#		#mod.index_go_into_es()
#		#mod.index_diseases_into_es()

if __name__ == '__main__':
	dataloader = DataLoader()
	dataloader.load_data()
