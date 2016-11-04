from intermine.webservice import Service
from mod import MOD


class SGD(MOD):
    species = "Saccharomyces cerevisiae"
    service = Service("http://yeastmine.yeastgenome.org/yeastmine/service")

    @staticmethod
    def gene_href(gene_id):
        return "http://www.yeastgenome.org/locus/" + gene_id + "/overview"

    @staticmethod
    def gene_id_from_panther(panther_id):
        # example: SGD=S000000226
        return panther_id.split("=")[1]

    def load_genes(self):
        genes = MOD.genes

        query = SGD.service.new_query("Gene")
        query.add_view(
            "primaryIdentifier", "secondaryIdentifier", "symbol", "name",
            "briefDescription", "sequenceOntologyTerm.name",
            "chromosome.primaryIdentifier", "chromosomeLocation.start",
            "chromosomeLocation.end", "chromosomeLocation.strand",
            "crossReferences.identifier", "crossReferences.dbxreftype",
            "organism.shortName"
        )
        query.add_constraint("organism.shortName", "=", "S. cerevisiae", code = "A")

        print("Fetching gene data from Yeastmine...")

        for row in query.rows():
            if row["symbol"] is None:
                continue

            if row["primaryIdentifier"] in genes:
                genes[row["primaryIdentifier"]]["external_ids"].append(row["crossReferences.dbxreftype"] + " " + row["crossReferences.identifier"])
            else:
                synonyms = []
                if row["secondaryIdentifier"]:
                    synonyms.append(row["secondaryIdentifier"])

                chromosomes = []
                if row["chromosome.primaryIdentifier"]:
                    chromosomes = [row["chromosome.primaryIdentifier"]]

                genes[row["primaryIdentifier"]] = {
                    "gene_symbol": row["symbol"],
                    "name": row["name"],
                    "description": row["briefDescription"],
                    "gene_synonyms": synonyms,
                    "gene_type": row["sequenceOntologyTerm.name"],
                    "gene_chromosomes": chromosomes,
                    "gene_chromosome_starts": row["chromosomeLocation.start"],
                    "gene_chromosome_ends": row["chromosomeLocation.end"],
                    "gene_chromosome_strand": row["chromosomeLocation.strand"],
                    "external_ids": [row["crossReferences.dbxreftype"] + " " + row["crossReferences.identifier"]],
                    "species": "Saccharomyces cerevisiae",

                    "gene_biological_process": [],
                    "gene_molecular_function": [],
                    "gene_cellular_component": [],

                    "homologs": [],

                    "name_key": row["symbol"].lower(),
                    "id": row["primaryIdentifier"],
                    "href": SGD.gene_href(row["primaryIdentifier"]),
                    "category": "gene"
                }

    def load_go(self):
        query = SGD.service.new_query("Gene")
        query.add_view(
            "primaryIdentifier", "symbol", "secondaryIdentifier",
            "goAnnotation.ontologyTerm.identifier", "goAnnotation.ontologyTerm.name",
            "goAnnotation.ontologyTerm.namespace"
        )
        query.add_constraint("organism.shortName", "=", "S. cerevisiae", code = "A")

        print("Fetching go data from Yeastmine...")
        for row in query.rows():
            self.add_go_annotation_to_gene(gene_id=row["primaryIdentifier"], go_id=row["goAnnotation.ontologyTerm.identifier"])

    def load_diseases(self):
        query = SGD.service.new_query("Gene")

        query.add_view(
            "primaryIdentifier", "secondaryIdentifier", "symbol",
            "homologues.homologue.primaryIdentifier", "homologues.homologue.symbol",
            "homologues.homologue.name",
            "homologues.homologue.crossReferences.identifier",
            "homologues.homologue.diseases.identifier",
            "homologues.homologue.diseases.name"
        )

        query.add_sort_order("Gene.symbol", "ASC")
        query.add_constraint("homologues.homologue.crossReferences.source.name", "=", "MIM", code = "D")
        query.add_constraint("homologues.homologue.organism.shortName", "=", "H. sapiens", code = "C")
        query.add_constraint("organism.shortName", "=", "S. cerevisiae", code = "B")
        query.add_constraint("homologues.dataSets.dataSource.name", "=", "Panther", code = "A")

        print("Fetching disease data from Yeastmine...")

        for row in query.rows():
            self.add_disease_annotation_to_gene(gene_id=row["primaryIdentifier"], omim_id='OMIM:' + row["homologues.homologue.diseases.identifier"])
