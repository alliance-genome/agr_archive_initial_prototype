from intermine.webservice import Service
from mod import MOD
import csv


class RGD(MOD):
	species = "Rattus norvegicus"
	service = Service("http://ratmine.mcw.edu/ratmine/service")

	@staticmethod
	def gene_href(gene_id):
		return "http://www.rgd.mcw.edu/rgdweb/report/gene/main.html?id=" + gene_id

	@staticmethod
	def get_organism_names():
		return ["Rattus norvegicus", "R. norvegicus", "RAT"]

	@staticmethod
	def gene_id_from_panther(panther_id):
		# example: RGD=628644
		return panther_id.replace("=", ":")

	def load_genes(self):
		return []

	def load_go(self):
		go_data_csv_filename = "data/rat_go.tsv"

		print("Fetching go data from RGD tsv file (" + go_data_csv_filename + ") ...")

		list = []
		with open(go_data_csv_filename, 'rb') as f:
			reader = csv.reader(f, delimiter='\t')

			for row in reader:
				list.append({"gene_id": row[5], "go_id": row[1], "species": RGD.species})
		return list

	def load_diseases(self):
		disease_data_csv_filename = "data/rat_disease.tsv"

		print("Fetching disease data from RGD tsv file (" + disease_data_csv_filename + ") ...")

		list = []
		with open(disease_data_csv_filename, 'rb') as f:
			reader = csv.reader(f, delimiter='\t')

			for row in reader:
				if (row[5].startswith("OMIM:")):
					list.append({"gene_id": row[0], "omim_id": row[5], "species": RGD.species})
		return list
