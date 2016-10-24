from intermine.webservice import Service
import mod


class Mouse():
    service = Service("http://www.mousemine.org/mousemine/service")

    @staticmethod
    def gene_href(gene_id):
        return "http://www.informatics.jax.org/marker/" + gene_id

    @staticmethod
    def load_genes(genes):
        query = Mouse.service.new_query("Gene")
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
                    "description": row["description"],
                    "gene_synonyms": [row["synonyms.value"]],
                    "gene_type": row["sequenceOntologyTerm.name"],
                    "gene_chromosomes": [row["chromosomeLocation.locatedOn.primaryIdentifier"]],
                    "gene_chromosome_starts": row["chromosomeLocation.start"],
                    "gene_chromosome_ends": row["chromosomeLocation.end"],
                    "gene_chromosome_strand": row["chromosomeLocation.strand"],
                    "external_ids": [cross_reference_link_type + " " + cross_reference_id],
                    "species": "Mus musculus",

                    "gene_biological_process": [],
                    "gene_molecular_function": [],
                    "gene_cellular_component": [],

                    "name_key": row["symbol"],
                    "href": Mouse.gene_href(row["primaryIdentifier"]),
                    "category": "gene"
                }

    @staticmethod
    def load_go(genes, go):
        query = Mouse.service.new_query("GOTerm")
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
            if row["identifier"] in ("GO:0008150", "GO:0003674", "GO:0005575"):
                continue

            gene = None
            if row["ontologyAnnotations.subject.primaryIdentifier"] and row["ontologyAnnotations.subject.symbol"]:
                gene = row["ontologyAnnotations.subject.symbol"].upper()

            if row["identifier"] in go:
                if gene:
                    go[row["identifier"]]["go_genes"].append(gene)

                if "Mus musculus" not in go[row["identifier"]]["go_species"]:
                    go[row["identifier"]]["go_species"].append("Mus musculus")
            else:
                go[row["identifier"]] = {
                    "name": row["name"],
                    "go_type": row["namespace"],
                    "go_genes": [gene],
                    "go_species": ["Mus musculus"],

                    "name_key": row["name"],
                    "href": "http://amigo.geneontology.org/amigo/term/" + row["identifier"],
                    "category": "go"
                }

            if row["namespace"] and row["ontologyAnnotations.subject.primaryIdentifier"] and row["ontologyAnnotations.subject.primaryIdentifier"] in genes:
                genes[row["ontologyAnnotations.subject.primaryIdentifier"]]["gene_" + row["namespace"]].append(row["name"])

    @staticmethod
    def load_diseases(gene, diseases):
        query = Mouse.service.new_query("OMIMTerm")
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
            if row["identifier"] in diseases:
                if row["ontologyAnnotations.subject.symbol"]:
                    diseases[row["identifier"]]["disease_genes"].append(row["ontologyAnnotations.subject.symbol"].upper())

                diseases[row["identifier"]]["disease_species"].append("Mus musculus")
            else:
                diseases[row["identifier"]] = {
                    "name": row["name"],
                    "disease_genes": [],
                    "disease_species": ["Mus musculus"],

                    "name_key": row["name"],
                    "href": "http://omim.org/entry/" + str(row["identifier"]),
                    "category": "disease"
                }

                if row["ontologyAnnotations.subject.symbol"]:
                    diseases[row["identifier"]]["disease_genes"].append(row["ontologyAnnotations.subject.symbol"].upper())
