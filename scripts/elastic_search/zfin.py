from intermine.webservice import Service


class ZFin():
    service = Service("http://www.zebrafishmine.org/service")

    @staticmethod
    def gene_href(gene_id):
        return "http://zfin.org/" + gene_id

    @staticmethod
    def load_genes(genes):
        query = ZFin.service.new_query("Gene")
        query.add_view(
            "name", "symbol", "primaryIdentifier", "organism.species",
            "crossReferences.identifier", "crossReferences.linkType",
            "sequenceOntologyTerm.identifier", "sequenceOntologyTerm.name",
            "chromosomes.name", "synonyms.value"
        )
        query.add_constraint("organism.species", "=", "rerio", code = "A")
        query.add_constraint("sequenceOntologyTerm.name", "=", "gene", code = "B")
        query.outerjoin("crossReferences")
        query.outerjoin("chromosomes")
        query.outerjoin("synonyms")

        print("Fetching gene data from ZebraFishMine...")

        for row in query.rows():
            if row["crossReferences.linkType"]:
                cross_reference_link_type = row["crossReferences.linkType"]
            else:
                cross_reference_link_type = ""

            if row["crossReferences.identifier"]:
                cross_reference_id = row["crossReferences.identifier"]
            else:
                cross_reference_id = ""

            if row["primaryIdentifier"] in genes:
                if row["synonyms.value"] is not None:
                    genes[row["primaryIdentifier"]]["gene_synonyms"].append(row["synonyms.value"])
                elif row["crossReferences.identifier"] is not None:
                    genes[row["primaryIdentifier"]]["external_ids"].append(cross_reference_link_type + " " + cross_reference_id)
                elif row["chromosomes.name"] is not None:
                    genes[row["primaryIdentifier"]]["gene_chromosomes"].append(row["chromosomes.name"])
            else:
                genes[row["primaryIdentifier"]] = {
                    "gene_symbol": row["symbol"],
                    "name": row["name"],
                    "description": None, # not present in ZFinMine
                    "gene_synonyms": [row["synonyms.value"]],
                    "gene_type": row["sequenceOntologyTerm.name"],
                    "gene_chromosomes": [row["chromosomes.name"]],
                    "gene_chromosome_starts": None,
                    "gene_chromosome_ends": None,
                    "gene_chromosome_strand": None,
                    "external_ids": [cross_reference_link_type + " " + cross_reference_id],
                    "species": "Danio renio",

                    "gene_biological_process": [],
                    "gene_molecular_function": [],
                    "gene_cellular_component": [],

                    "name_key": row["symbol"],
                    "href": ZFin.gene_href(row["primaryIdentifier"]),
                    "category": "gene"
                }

    @staticmethod
    def load_go(genes, go):
        query = ZFin.service.new_query("Gene")
        query.add_view(
            "name", "primaryIdentifier", "symbol",
            "goAnnotation.ontologyTerm.identifier", "goAnnotation.ontologyTerm.name",
            "organism.taxonId", "goAnnotation.ontologyTerm.namespace"
        )
        query.add_constraint("organism.taxonId", "=", "7955", code = "A")

        print ("Fetching go data from ZebraFishMine...")

        for row in query.rows():
            if row["goAnnotation.ontologyTerm.identifier"] in ("GO:0008150", "GO:0003674", "GO:0005575"):
                continue

            gene = None
            if row["primaryIdentifier"] in genes and genes[row["primaryIdentifier"]]["gene_symbol"]:
                gene = genes[row["primaryIdentifier"]]["gene_symbol"].upper()

            if row["goAnnotation.ontologyTerm.identifier"] in go:
                if gene:
                    go[row["goAnnotation.ontologyTerm.identifier"]]["go_genes"].append(gene)
                go[row["goAnnotation.ontologyTerm.identifier"]]["go_species"].append("Danio renio")
            else:
                go[row["goAnnotation.ontologyTerm.identifier"]] = {
                    "name": row["goAnnotation.ontologyTerm.name"],
                    "go_type": row["goAnnotation.ontologyTerm.namespace"],
                    "go_genes": [gene],
                    "go_species": ["Danio renio"],

                    "name_key": row["goAnnotation.ontologyTerm.name"],
                    "href": "http://amigo.geneontology.org/amigo/term/" + row["goAnnotation.ontologyTerm.identifier"],
                    "category": "go"
                }

            if row["primaryIdentifier"] in genes:
                if row["goAnnotation.ontologyTerm.namespace"]:
                    genes[row["primaryIdentifier"]]["gene_" + row["goAnnotation.ontologyTerm.namespace"]].append(row["goAnnotation.ontologyTerm.name"])

    @staticmethod
    def load_diseases(genes, diseases):
        query = ZFin.service.new_query("OmimPhenotype")
        query.add_view(
            "disease", "phenotypeLink.identifier", "phenotypeLink.linkType",
            "genes.primaryIdentifier", "genes.symbol", "genes.name"
        )
        query.outerjoin("phenotypeLink")

        print ("Fetching disease data from ZebraFishMine...")

        for row in query.rows():
            if row["phenotypeLink.identifier"] in diseases:
                diseases[row["phenotypeLink.identifier"]]["disease_genes"].append(row["genes.symbol"])
                diseases[row["phenotypeLink.identifier"]]["disease_species"].append("Danio renio")
            else:
                diseases[row["phenotypeLink.identifier"]] = {
                    "name": row["disease"],
                    "disease_genes": [row["genes.symbol"]],
                    "disease_species": ["Danio renio"],

                    "name_key": row["disease"],
                    "href": "http://omim.org/entry/" + str(row["phenotypeLink.identifier"]),
                    "category": "disease"
                }
