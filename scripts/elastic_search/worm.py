import xlrd
import csv


class Worm():
    @staticmethod
    def gene_href(gene_id):
        return "http://www.wormbase.org/species/c_elegans/gene/" + gene_id

    @staticmethod
    def load_genes(genes):
        gene_data_xls_filename = "data/WormBase_C_elegans_gene_total_info.xlsx.xlsx"

        print("Fetching gene data from WormBase xlsx file...")

        workbook = xlrd.open_workbook(gene_data_xls_filename)
        sheet = workbook.sheet_by_index(0)

        for i in range(1, sheet.nrows):
            row = sheet.row(i)

            if row[3].value == "":
                gene_type = None
            else:
                gene_type = row[3].value

            genes[row[0].value] = {
                "gene_symbol": row[1].value,
                "name": row[1].value,
                "description": row[4].value,
                "gene_synonyms": map(lambda s: s.strip(), row[9].value.split(",")),
                "gene_type": gene_type,
                "gene_chromosomes": [row[5].value],
                "gene_chromosome_starts": row[6].value,
                "gene_chromosome_ends": row[7].value,
                "gene_chromosome_strand": row[8].value,
                "external_ids": [],
                "species": "Caenorhabditis elegans",

                "gene_biological_process": [],
                "gene_molecular_function": [],
                "gene_cellular_component": [],

                "name_key": row[1].value,
                "href": Worm.gene_href(row[0].value),
                "category": "gene"
            }

    @staticmethod
    def load_go(genes, go):
        go_data_csv_filename = "data/GO_terms_and_synonyms_(WormBase).txt"

        print("Fetching go data from WormBase txt file...")

        with open(go_data_csv_filename, 'rb') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                if row[0] in ("GO:0008150", "GO:0003674", "GO:0005575"):
                    continue

                if row[0] in go:
                    go[row[0]]["go_species"].append("Caenorhabditis elegans")
                else:
                    go[row[0]] = {
                        "name": row[1],
                        "go_type": row[2].lower(),
                        "go_genes": [],
                        "go_species": ["Caenorhabditis elegans"],

                        "name_key": row[1],
                        "href": "http://amigo.geneontology.org/amigo/term/" + row[0],
                        "category": "go"
                    }

    @staticmethod
    def load_diseases(genes, diseases):
        disease_data_csv_filename = "data/Diseases_OMIM_IDs_and_synonyms_(WormBase).txt"

        print("Fetching disease data from WormBase txt file...")

        with open(disease_data_csv_filename, 'rb') as f:
            reader = csv.reader(f, delimiter='\t')
            next(reader, None)

            for row in reader:
                if row[2] and row[2] != "":
                    omim_ids = map(lambda s: s.strip(), row[2].split(","))

                    for omim_id in omim_ids:
                        if omim_id in diseases:
                            diseases[omim_id]["disease_species"].append("Caenorhabditis elegans")
                        else:
                            diseases[omim_id] = {
                                "name": row[1],
                                "disease_genes": [],
                                "disease_species": ["Caenorhabditis elegans"],

                                "name_key": row[1],
                                "href": "http://omim.org/entry/" + str(omim_id),
                                "category": "disease"
                            }
