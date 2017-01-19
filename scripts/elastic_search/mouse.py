from mod import MOD
from intermine.webservice import Service


class MGI(MOD):
    species = "Mus musculus"
    service = Service("http://www.mousemine.org/mousemine/service")

    @staticmethod
    def gene_href(gene_id):
        return "http://www.informatics.jax.org/marker/" + gene_id

    @staticmethod
    def gene_id_from_panther(panther_id):
        # example: MGI=MGI=1924210
        return ":".join(panther_id.split("=")[1:]).strip()

    def load_genes(self):
        genes = MOD.genes

        query = MGI.service.new_query("Gene")
        query.add_view(
            "primaryIdentifier", "symbol", "name", "description",
            "sequenceOntologyTerm.name", "organism.shortName",
            "chromosomeLocation.locatedOn.primaryIdentifier",
            "chromosomeLocation.start", "chromosomeLocation.end",
            "chromosomeLocation.strand", "crossReferences.identifier",
            "crossReferences.source.name", "synonyms.value"
        )
        query.add_constraint("organism.shortName", "=", "M. musculus", code = "A")
        query.add_constraint("dataSets.name", "=", "Mouse Gene Catalog from MGI", code = "B")
        query.outerjoin("chromosomeLocation")
        query.outerjoin("chromosomeLocation.locatedOn")
        query.outerjoin("crossReferences")
        query.outerjoin("crossReferences.source")
        query.outerjoin("synonyms")

        print("Fetching gene data from MouseMine...")

        for row in query.rows():
            if row["crossReferences.source.name"]:
                cross_reference_link_type = row["crossReferences.source.name"]
            else:
                cross_reference_link_type = ""

            if row["crossReferences.identifier"]:
                cross_reference_id = row["crossReferences.identifier"]
            else:
                cross_reference_id = ""

            if row["primaryIdentifier"] in genes:
                if row["synonyms.value"]:
                    genes[row["primaryIdentifier"]]["gene_synonyms"].append(row["synonyms.value"])
                if row["crossReferences.identifier"]:
                    genes[row["primaryIdentifier"]]["external_ids"].append(cross_reference_link_type + " " + cross_reference_id)
                if row["chromosomeLocation.locatedOn.primaryIdentifier"] and row["chromosomeLocation.locatedOn.primaryIdentifier"] not in genes[row["primaryIdentifier"]]["gene_chromosomes"]:
                    genes[row["primaryIdentifier"]]["gene_chromosomes"].append(row["chromosomeLocation.locatedOn.primaryIdentifier"])
            else:
                synonyms = []
                if row["synonyms.value"]:
                    synonyms.append(row["synonyms.value"])

                chromosomes = []
                if row["chromosomeLocation.locatedOn.primaryIdentifier"]:
                    chromosomes = [row["chromosomeLocation.locatedOn.primaryIdentifier"]]

                genes[row["primaryIdentifier"]] = {
                    "gene_symbol": row["symbol"],
                    "name": row["name"],
                    "description": row["description"],
                    "gene_synonyms": synonyms,
                    "gene_type": row["sequenceOntologyTerm.name"],
                    "gene_chromosomes": chromosomes,
                    "gene_chromosome_starts": row["chromosomeLocation.start"],
                    "gene_chromosome_ends": row["chromosomeLocation.end"],
                    "gene_chromosome_strand": row["chromosomeLocation.strand"],
                    "external_ids": [cross_reference_link_type + " " + cross_reference_id],
                    "species": "Mus musculus",

                    "gene_biological_process": [],
                    "gene_molecular_function": [],
                    "gene_cellular_component": [],

                    "homologs": [],

                    "name_key": row["symbol"].lower(),
                    "id": row["primaryIdentifier"],
                    "href": MGI.gene_href(row["primaryIdentifier"]),
                    "category": "gene"
                }

    def load_go(self):
        query = MGI.service.new_query("GOTerm")
        query.add_constraint("ontologyAnnotations.subject", "SequenceFeature")
        query.add_view(
            "identifier", "name", "namespace", "ontologyAnnotations.qualifier",
            "ontologyAnnotations.subject.primaryIdentifier",
            "ontologyAnnotations.subject.symbol", "synonyms.name", "synonyms.type"
        )
        query.outerjoin("ontologyAnnotations")
        query.outerjoin("ontologyAnnotations.subject")
        query.outerjoin("synonyms")

        print ("Fetching go data from MouseMine...")

        for row in query.rows():
            self.add_go_annotation_to_gene(gene_id=row["ontologyAnnotations.subject.primaryIdentifier"], go_id=row["identifier"])

    def load_diseases(self):
        query = MGI.service.new_query("OMIMTerm")
        query.add_constraint("ontologyAnnotations.subject", "SequenceFeature")
        query.add_view(
            "identifier", "name", "synonyms.name", "synonyms.type",
            "ontologyAnnotations.qualifier",
            "ontologyAnnotations.subject.primaryIdentifier",
            "ontologyAnnotations.subject.symbol"
        )
        query.add_constraint("ontologyAnnotations.subject.organism.taxonId", "=", "10090", code = "A")
        query.outerjoin("synonyms")
        query.outerjoin("ontologyAnnotations")

        print ("Fetching disease data from MouseMine...")

        for row in query.rows():
            self.add_disease_annotation_to_gene(gene_id=row["ontologyAnnotations.subject.primaryIdentifier"], omim_id=row["identifier"])
