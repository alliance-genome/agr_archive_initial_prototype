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
    def gene_id_from_panther(panther_id):
        # example: RGD=628644
        return panther_id.replace("=", ":")

    def load_genes(self):
        genes = MOD.genes

        query = RGD.service.new_query("Gene")
        query.add_view(
            "symbol", "name", "primaryIdentifier", "chromosome.organism.commonName",
            "chromosome.primaryIdentifier", "synonyms.value", "description",
            "sequenceOntologyTerm.name", "locations.end", "locations.start",
            "locations.strand"
        )

        query.add_constraint("organism.commonName", "=", "Norway rat", code = "A")

        print("Fetching gene data from RatMine...")

        for row in query.rows():
            if row["primaryIdentifier"] in genes:
                if row["synonyms.value"]:
                    genes[row["primaryIdentifier"]]["gene_synonyms"].append(row["synonyms.value"])
            else:
                synonyms = []
                if row["synonyms.value"]:
                    synonyms.append(row["synonyms.value"])

                chromosomes = []
                if row["chromosome.primaryIdentifier"]:
                    chromosomes = [row["chromosome.primaryIdentifier"]]

                genes[row["primaryIdentifier"]] = {
                    "gene_symbol": row["symbol"],
                    "name": row["name"],
                    "description": row["description"],
                    "gene_synonyms": synonyms,
                    "gene_type": row["sequenceOntologyTerm.name"],
                    "gene_chromosomes": chromosomes,
                    "gene_chromosome_starts": row["locations.start"],
                    "gene_chromosome_ends": row["locations.end"],
                    "gene_chromosome_strand": row["locations.strand"],
                    "external_ids": [],
                    "species": "Rattus norvegicus",

                    "gene_biological_process": [],
                    "gene_molecular_function": [],
                    "gene_cellular_component": [],

                    "homologs": [],

                    "name_key": row["symbol"],
                    "id": row["primaryIdentifier"],
                    "href": RGD.gene_href(row["primaryIdentifier"]),
                    "category": "gene"
                }

    def load_go(self):
        go_data_csv_filename = "data/rat_go.tsv"

        print("Fetching go data from RGD tsv file...")

        with open(go_data_csv_filename, 'rb') as f:
            reader = csv.reader(f, delimiter='\t')

            for row in reader:
                self.add_go_annotation_to_gene(gene_id=row[5], go_id=row[1])

    def load_diseases(self):
        disease_data_csv_filename = "data/rat_disease.tsv"

        print("Fetching disease data from RGD tsv file...")

        with open(disease_data_csv_filename, 'rb') as f:
            reader = csv.reader(f, delimiter='\t')

            for row in reader:
                if (row[5].startswith("OMIM:")):
                    self.add_disease_annotation_to_gene(gene_id=row[0], omim_id=row[5])
