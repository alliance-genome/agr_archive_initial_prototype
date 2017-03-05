from files import *
from mods.human import Human

class HomoLogLoader:

    def __init__(self, mods):
        path = "tmp"
        S3File("mod-datadumps", "RefGenomeOrthologs.tar.gz", path).download()
        TARFile(path, "RefGenomeOrthologs.tar.gz").extract_all()
        self.homolog_data = CSVFile(path + "/" + "RefGenomeOrthologs").get_data()

        self.organism_to_mods = {}
        for mod in mods:
            for organism in mod.get_organism_names():
                self.organism_to_mods[organism] = mod

        if "HUMAN" not in self.organism_to_mods:
            human = Human()
            for organism in Human.get_organism_names():
                self.organism_to_mods[organism] = human

    def attach_homolog_data(self, genes):

        for row in self.homolog_data:

            gene_1 = self._process_gene_id_from_panther(row[0], genes)
            gene_2 = self._process_gene_id_from_panther(row[1], genes)

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

    def _process_gene_id_from_panther(self, gene_ids_panther, genes):
        gene_ids = gene_ids_panther.split("|")

        if gene_ids[0] in self.organism_to_mods:
            mod = self.organism_to_mods[gene_ids[0]]
        else:
            return None

        gene_id = mod.gene_id_from_panther(gene_ids[1])

        gene_symbol = ""
        if mod.__class__.__module__ == "human":
            gene_symbol = gene_id
        else:
            if gene_id not in genes:
                return None
            else:
                gene_symbol = genes[gene_id]["symbol"]

        return {
            "id": gene_id,
            "symbol": gene_symbol,
            "href": mod.gene_href(gene_id),
            "species": mod.species
        }
