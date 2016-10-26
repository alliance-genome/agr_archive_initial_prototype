import csv


class Fly():
    @staticmethod
    def gene_href(gene_id):
        return "http://flybase.org/reports/" + gene_id + ".html"

    @staticmethod
    def load_genes(genes):
        genes_data_csv_filename = "data/FlyBase_Genes_output_fb_2016_04.tsv"

        print("Fetching gene data from FlyBase tsv file...")

        with open(genes_data_csv_filename, 'rb') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                genes[row[0]] = {
                    "gene_symbol": row[1],
                    "name": row[1],
                    "description": row[4],
                    "gene_synonyms": map(lambda s: s.strip(), row[9].split(",")),
                    "gene_type": row[3],
                    "gene_chromosomes": [row[5]],
                    "gene_chromosome_starts": row[6],
                    "gene_chromosome_ends": row[7],
                    "gene_chromosome_strand": row[8],
                    "external_ids": [],
                    "species": "Drosophila melanogaster",

                    "gene_biological_process": [],
                    "gene_molecular_function": [],
                    "gene_cellular_component": [],

                    "name_key": row[1],
                    "href": Fly.gene_href(row[0]),
                    "category": "gene"
                }

    @staticmethod
    def load_go(genes, go):
        go_data_csv_filename = "data/FlyBase_GO_output_fb_2016_04.tsv"

        print("Fetching go data from FlyBase tsv file...")

        with open(go_data_csv_filename, 'rb') as f:
            reader = csv.reader(f, delimiter='\t')

            for row in reader:
                if 'GO:' + row[2].lower() in ("GO:0008150", "GO:0003674", "GO:0005575"):
                    continue

                go_genes = map(lambda s: s.strip(), row[4].split(","))

                go_gene_symbols = []
                for gene in go_genes:
                    if gene in genes and genes[gene]["gene_symbol"]:
                        go_gene_symbols.append(genes[gene]["gene_symbol"].upper())

                if ('GO:' + row[2]) in go:
                    go['GO:' + row[2]]["go_genes"] += go_gene_symbols
                    go['GO:' + row[2]]["go_species"].append("Drosophila melanogaster")
                else:
                    go['GO:' + row[2]] = {
                        "name": row[0],
                        "go_type": row[3].lower(),
                        "go_genes": go_gene_symbols,
                        "go_species": ["Drosophila melanogaster"],

                        "name_key": row[0],
                        "href": "http://amigo.geneontology.org/amigo/term/GO:" + row[2],
                        "category": "go"
                    }

                for gene in go_genes:
                    if gene in genes:
                        genes[gene]["gene_" + row[3].lower()].append(row[0])

    @staticmethod
    def load_diseases(genes, diseases):
        diseases_data_csv_filename = "data/FlyBase_DOID_output_fb_2016_04.tsv"

        print("Fetching disease data from FlyBase tsv file...")

        with open(diseases_data_csv_filename, 'rb') as f:
            reader = csv.reader(f, delimiter='\t')
            next(reader, None)

            for row in reader:
                if row[3]:
                    omim_ids = map(lambda s: s.strip(), row[3].split(","))
                    disease_gene_ids = map(lambda s: s.strip(), row[5].split(","))
                    disease_genes = set([])
                    for gene in disease_gene_ids:
                        if gene in genes:
                            disease_genes.add(genes[gene]["gene_symbol"].upper())

                    for omim_id in omim_ids:
                        if omim_id in diseases:
                            diseases[omim_id]["disease_genes"] += disease_genes
                            diseases[omim_id]["disease_species"] += ["Drosophila melanogaster"]
                        else:
                            diseases[omim_id] = {
                                "name": row[1],
                                "disease_genes": list(disease_genes),
                                "disease_species": ["Drosophila melanogaster"],

                                "name_key": row[1],
                                "href": "http://omim.org/entry/" + str(omim_id),
                                "category": "disease"
                            }
