from intermine.webservice import Service
from loaders.gene_loader import GeneLoader
from mod import MOD

class ZFIN(MOD):
	species = "Danio rerio"
	service = Service("http://www.zebrafishmine.org/service")

	@staticmethod
	def gene_href(gene_id):
		return "http://zfin.org/" + gene_id

	@staticmethod
	def get_organism_names():
		return ["Danio rerio", "D. rerio", "DANRE"]

	@staticmethod
	def gene_id_from_panther(panther_id):
		# example: ZFIN=ZDB-GENE-050522-480
		return panther_id.split("=")[1]

	def load_genes(self):
		return GeneLoader("data/basic-gene-info-zfin.json").get_data()

	def load_go(self):
		query = ZFIN.service.new_query("Gene")
		query.add_view(
			"name", "primaryIdentifier", "symbol",
			"goAnnotation.ontologyTerm.identifier", "goAnnotation.ontologyTerm.name",
			"organism.taxonId", "goAnnotation.ontologyTerm.namespace"
		)
		query.add_constraint("organism.taxonId", "=", "7955", code = "A")

		print ("Fetching go data from ZebraFishMine...")

		list = []
		for row in query.rows():
			list.append({"gene_id": row["primaryIdentifier"], "go_id": row["goAnnotation.ontologyTerm.identifier"], "species": ZFIN.species})
		return list

	def load_diseases(self):
		query = ZFIN.service.new_query("OmimPhenotype")
		query.add_view(
			"disease", "phenotypeLink.identifier", "phenotypeLink.linkType",
			"genes.primaryIdentifier", "genes.symbol", "genes.name"
		)
		query.outerjoin("phenotypeLink")

		print ("Fetching disease data from ZebraFishMine...")

		list = []
		for row in query.rows():
			if row["phenotypeLink.identifier"] is not None:
				list.append({"gene_id": row["genes.primaryIdentifier"], "omim_id": "OMIM:"+row["phenotypeLink.identifier"], "species": ZFIN.species})
		return list
