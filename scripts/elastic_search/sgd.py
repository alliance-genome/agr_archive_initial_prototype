from intermine.webservice import Service
import mod


class SGD():
    service = Service("http://yeastmine.yeastgenome.org/yeastmine/service")

    @staticmethod
    def gene_href(gene_id):
        return "http://www.yeastgenome.org/locus/" + gene_id + "/overview"

    @staticmethod
    def load_genes(genes):
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
            if row["primaryIdentifier"] in genes:
                genes[row["primaryIdentifier"]]["external_ids"].append(row["crossReferences.dbxreftype"] + " " + row["crossReferences.identifier"])
            else:
                genes[row["primaryIdentifier"]] = {
                    "gene_symbol": row["symbol"],
                    "name": row["name"],
                    "description": row["briefDescription"],
                    "gene_synonyms": [row["secondaryIdentifier"]],
                    "gene_type": row["sequenceOntologyTerm.name"],
                    "gene_chromosomes": [row["chromosome.primaryIdentifier"]],
                    "gene_chromosome_starts": row["chromosomeLocation.start"],
                    "gene_chromosome_ends": row["chromosomeLocation.end"],
                    "gene_chromosome_strand": row["chromosomeLocation.strand"],
                    "external_ids": [row["crossReferences.dbxreftype"] + " " + row["crossReferences.identifier"]],
                    "species": "Saccharomyces cerevisiae",

                    "gene_biological_process": [],
                    "gene_molecular_function": [],
                    "gene_cellular_component": [],

                    "name_key": row["symbol"],
                    "href": SGD.gene_href(row["primaryIdentifier"]),
                    "category": "gene"
                }

    @staticmethod
    def load_go(genes, go):
        query = SGD.service.new_query("Gene")
        query.add_view(
            "primaryIdentifier", "symbol", "secondaryIdentifier",
            "goAnnotation.ontologyTerm.identifier", "goAnnotation.ontologyTerm.name",
            "goAnnotation.ontologyTerm.namespace"
        )
        query.add_constraint("organism.shortName", "=", "S. cerevisiae", code = "A")

        print("Fetching go data from Yeastmine...")

        for row in query.rows():
            if row["goAnnotation.ontologyTerm.identifier"] in ("GO:0008150", "GO:0003674", "GO:0005575"):
                continue

            gene = None
            if row["primaryIdentifier"] in genes and genes[row["primaryIdentifier"]]["gene_symbol"]:
                gene = genes[row["primaryIdentifier"]]["gene_symbol"].upper()

            if row["goAnnotation.ontologyTerm.identifier"] in go:
                if gene:
                    go[row["goAnnotation.ontologyTerm.identifier"]]["go_genes"].append(gene)
                go[row["goAnnotation.ontologyTerm.identifier"]]["go_species"].append("Saccharomyces cerevisiae")
            else:
                go[row["goAnnotation.ontologyTerm.identifier"]] = {
                    "name": row["goAnnotation.ontologyTerm.name"],
                    "go_type": row["goAnnotation.ontologyTerm.namespace"],
                    "go_genes": [gene],
                    "go_species": ["Saccharomyces cerevisiae"],

                    "name_key": row["goAnnotation.ontologyTerm.name"],
                    "href": "http://amigo.geneontology.org/amigo/term/" + row["goAnnotation.ontologyTerm.identifier"],
                    "category": "go"
                }

                if row["primaryIdentifier"] in genes:
                    genes[row["primaryIdentifier"]]["gene_" + row["goAnnotation.ontologyTerm.namespace"]].append(row["goAnnotation.ontologyTerm.name"])

    @staticmethod
    def load_diseases(genes, diseases):
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
            if row["homologues.homologue.diseases.identifier"] in diseases:
                diseases[row["homologues.homologue.diseases.identifier"]]["disease_genes"].append(row["symbol"])
                diseases[row["homologues.homologue.diseases.identifier"]]["disease_species"].append("Saccharomyces cerevisiae")
            else:
                diseases[row["homologues.homologue.diseases.identifier"]] = {
                    "name": row["homologues.homologue.diseases.name"],
                    "disease_genes": [row["symbol"]],
                    "disease_species": ["Saccharomyces cerevisiae"],

                    "name_key": row["homologues.homologue.diseases.name"],
                    "href": "http://omim.org/entry/" + str(row["homologues.homologue.diseases.identifier"]),
                    "category": "disease"
                }
