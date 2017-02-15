from files import *
from mods import *

class DataLoader:
	gene_bkp_filename = "data/genes_bkp.pickle"
	go_bkp_filename = "data/go_bkp.pickle"
	so_bkp_filename = "data/so_bkp.pickle"
	diseases_bkp_filename = "data/diseases_bkp.pickle"

	def load_data():
		mods = [MGI(), ZFIN(), SGD(), WormBase(), FlyBase(), RGD()]

		genes = []
		go = []
		so = []
		diseases = []

		for m in mods:
			genes.append(m.load_genes())

		load_homologs(genes)

		for m in mods:
			m.load_go()
			m.load_diseases()
		
		PickleFile(self.gene_bkp_filename).save(genes)
		PickleFile(self.go_bkp_filename).save(go)
		PickleFile(self.diseases_bkp_filename).save(diseases)
		#PickleFile(self.so_bkp_filename).save(so)

	def load_homologs(self, genes):
		homolog_data = CVSFile("data/RefGenomeOrthologs").get_data()
		for row in reader:

			gene_1 = MOD._process_gene_id_from_panther(row[0], self.genes)
			gene_2 = MOD._process_gene_id_from_panther(row[1], self.genes)

				if gene_1 is None or gene_2 is None:
					continue

				if gene_1["species"] != Human.species:
					if "homologs" not in self.genes[gene_1["id"]]:
						self.genes[gene_1["id"]]["homologs"] = []

					self.genes[gene_1["id"]]["homologs"].append({
						"symbol": gene_2["symbol"],
						"href": gene_2["href"],
						"species": gene_2["species"],
						"relationship_type": row[2],
						"ancestral": row[3],
						"panther_family": row[4]
					})

				if gene_2["species"] != Human.species:
					if "homologs" not in self.genes[gene_2["id"]]:
						self.genes[gene_2["id"]]["homologs"] = []

					self.genes[gene_2["id"]]["homologs"].append({
						"symbol": gene_1["symbol"],
						"href": gene_1["href"],
						"species": gene_1["species"],
						"relationship_type": row[2],
						"ancestral": row[3],
						"panther_family": row[4]
					})



	def delete_mapping(self):
		print "Deleting mapping..."
		response = requests.delete(os.environ['ES_URI'] + self.INDEX_NAME + "/")
		if response.status_code != 200:
			print "ERROR: " + str(response.json())
		else:
			print "SUCCESS"

	def put_mapping(self):
		from mapping import mapping

		print "Putting mapping... "
		response = requests.put(os.environ['ES_URI'] + self.INDEX_NAME + "/", json=mapping)
		if response.status_code != 200:
			print "ERROR: " + str(response.json())
		else:
			print "SUCCESS"

	def index_all_into_es(self):
		self.index_genes_into_es()
		self.index_go_into_es()
		self.index_diseases_into_es()
	def index_into_es(self, data):
		bulk_data = []

		for id in data:
			bulk_data.append({
				'index': {
					'_index': self.INDEX_NAME,
					'_type': self.DOC_TYPE,
					'_id': id
				}
			})
			bulk_data.append(data[id])

			if len(bulk_data) == 300:
				self.es.bulk(index=self.INDEX_NAME, body=bulk_data, refresh=True)
				bulk_data = []

		if len(bulk_data) > 0:
			self.es.bulk(index=self.INDEX_NAME, body=bulk_data, refresh=True)

	def index_genes_into_es(self):
		print "Indexing genes into ES..."
		self.index_into_es(self.genes)

	def index_go_into_es(self):
		print "Indexing go into ES..."
		self.index_into_es(self.go)

	def index_diseases_into_es(self):
		print "Indexing diseases into ES..."
		self.index_into_es(self.diseases)


mod.index_genes_into_es()
mod.index_go_into_es()
mod.index_diseases_into_es()
		pass

if __name__ == '__main__':
	dataloader = DataLoader()
	dataloader.load_data()
