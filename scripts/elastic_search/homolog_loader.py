
class HomoLogLoader:

	def __init__():
		self.homolog_data = CVSFile("data/RefGenomeOrthologs").get_data()

	def attach_homolog_data(genes):
		for row in homolog_data:

			gene_1 = MOD._process_gene_id_from_panther(row[0], genes)
			gene_2 = MOD._process_gene_id_from_panther(row[1], genes)

			if gene_1 is None or gene_2 is None:
				continue

			if gene_1["species"] != Human.species:
				if "homologs" not in genes[gene_1["id"]]:
					genes[gene_1["id"]]["homologs"] = []

				genes[gene_1["id"]]["homologs"].append({
					"symbol": gene_2["symbol"],
					"href": gene_2["href"],
					"species": gene_2["species"],
					"relationship_type": row[2],
					"ancestral": row[3],
					"panther_family": row[4]
				})

			if gene_2["species"] != Human.species:
				if "homologs" not in genes[gene_2["id"]]:
					genes[gene_2["id"]]["homologs"] = []

				genes[gene_2["id"]]["homologs"].append({
					"symbol": gene_1["symbol"],
					"href": gene_1["href"],
					"species": gene_1["species"],
					"relationship_type": row[2],
					"ancestral": row[3],
					"panther_family": row[4]
				})

