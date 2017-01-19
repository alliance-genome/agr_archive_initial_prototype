from intermine.webservice import Service
from mod import MOD


class ZFin(MOD):
    species = "Danio rerio"
    service = Service("http://www.zebrafishmine.org/service")

    @staticmethod
    def gene_href(gene_id):
        return "http://zfin.org/" + gene_id

    @staticmethod
    def gene_id_from_panther(panther_id):
        # example: ZFIN=ZDB-GENE-050522-480
        return panther_id.split("=")[1]

    def load_genes(self):
        genes = MOD.genes

        query = ZFin.service.new_query("Gene")
        query.add_view(
            "name", "symbol", "primaryIdentifier", "organism.species",
            "crossReferences.identifier", "crossReferences.linkType",
            "sequenceOntologyTerm.identifier", "sequenceOntologyTerm.name",
            "chromosomes.name", "synonyms.value"
        )
        query.add_constraint("organism.species", "=", "rerio", code = "A")
        query.add_constraint("sequenceOntologyTerm.name", "=", "gene", code = "B")
        query.add_constraint("synonyms.value", "!=", "ZDB-*", code = "C")
        query.outerjoin("crossReferences")
        query.outerjoin("chromosomes")

        print("Fetching gene data from ZebraFishMine...")

        for row in query.rows():
            if row["symbol"] is None:
                continue

            if row["crossReferences.linkType"]:
                cross_reference_link_type = row["crossReferences.linkType"]
            else:
                cross_reference_link_type = ""

            if row["crossReferences.identifier"]:
                cross_reference_id = row["crossReferences.identifier"]
            else:
                cross_reference_id = ""

            if row["primaryIdentifier"] in genes:
                if row["synonyms.value"] is not None and row["synonyms.value"] not in genes[row["primaryIdentifier"]]["gene_synonyms"]:
                    genes[row["primaryIdentifier"]]["gene_synonyms"].append(row["synonyms.value"])
                elif row["crossReferences.identifier"] is not None:
                    genes[row["primaryIdentifier"]]["external_ids"].append(cross_reference_link_type + " " + cross_reference_id)
                elif row["chromosomes.name"] is not None and row["chromosomes.name"] not in genes[row["primaryIdentifier"]]["gene_chromosomes"]:
                    genes[row["primaryIdentifier"]]["gene_chromosomes"].append(row["chromosomes.name"])
            else:
                synonyms = []
                if row["synonyms.value"]:
                    synonyms = [row["synonyms.value"]]

                chromosomes = []
                if row["chromosomes.name"]:
                    chromosomes = [row["chromosomes.name"]]

                genes[row["primaryIdentifier"]] = {
                    "gene_symbol": row["symbol"],
                    "name": row["name"],
                    "description": None, # not present in ZFinMine
                    "gene_synonyms": synonyms,
                    "gene_type": row["sequenceOntologyTerm.name"],
                    "gene_chromosomes": chromosomes,
                    "gene_chromosome_starts": None,
                    "gene_chromosome_ends": None,
                    "gene_chromosome_strand": None,
                    "external_ids": [cross_reference_link_type + " " + cross_reference_id],
                    "species": "Danio rerio",

                    "gene_biological_process": [],
                    "gene_molecular_function": [],
                    "gene_cellular_component": [],

                    "homologs": [],

                    "name_key": row["symbol"].lower(),
                    "id": row["primaryIdentifier"],
                    "href": ZFin.gene_href(row["primaryIdentifier"]),
                    "category": "gene"
                }

    def load_go(self):
        query = ZFin.service.new_query("Gene")
        query.add_view(
            "name", "primaryIdentifier", "symbol",
            "goAnnotation.ontologyTerm.identifier", "goAnnotation.ontologyTerm.name",
            "organism.taxonId", "goAnnotation.ontologyTerm.namespace"
        )
        query.add_constraint("organism.taxonId", "=", "7955", code = "A")

        print ("Fetching go data from ZebraFishMine...")

        for row in query.rows():
            self.add_go_annotation_to_gene(gene_id=row["primaryIdentifier"], go_id=row["goAnnotation.ontologyTerm.identifier"])

    def load_diseases(self):
        query = ZFin.service.new_query("OmimPhenotype")
        query.add_view(
            "disease", "phenotypeLink.identifier", "phenotypeLink.linkType",
            "genes.primaryIdentifier", "genes.symbol", "genes.name"
        )
        query.outerjoin("phenotypeLink")

        print ("Fetching disease data from ZebraFishMine...")

        for row in query.rows():
            if row["phenotypeLink.identifier"] is not None:
                self.add_disease_annotation_to_gene(gene_id=row["genes.primaryIdentifier"], omim_id="OMIM:"+row["phenotypeLink.identifier"])
