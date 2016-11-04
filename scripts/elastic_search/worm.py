from mod import MOD
import xlrd
import csv


class WormBase(MOD):
    species = "Caenorhabditis elegans"

    @staticmethod
    def gene_href(gene_id):
        return "http://www.wormbase.org/species/c_elegans/gene/" + gene_id

    @staticmethod
    def gene_id_from_panther(panther_id):
        # example: WormBase=WBGene00004831
        return panther_id.split("=")[1]

    def load_genes(self):
        genes = MOD.genes

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

            chromosomes = []
            if row[5].value:
                chromosomes = [row[5].value]

            genes[row[0].value] = {
                "gene_symbol": row[1].value,
                "name": row[1].value,
                "description": row[4].value,
                "gene_synonyms": map(lambda s: s.strip(), row[9].value.split(",")),
                "gene_type": gene_type,
                "gene_chromosomes": chromosomes,
                "gene_chromosome_starts": row[6].value,
                "gene_chromosome_ends": row[7].value,
                "gene_chromosome_strand": row[8].value,
                "external_ids": [],
                "species": "Caenorhabditis elegans",

                "gene_biological_process": [],
                "gene_molecular_function": [],
                "gene_cellular_component": [],

                "homologs": [],

                "name_key": row[1].value.lower(),
                "id": row[0].value,
                "href": WormBase.gene_href(row[0].value),
                "category": "gene"
            }

    def load_go(self):
        go_data_csv_filename = "data/wormbase_gene_association.tsv"

        print("Fetching go data from WormBase txt file...")

        with open(go_data_csv_filename, 'rb') as f:
            reader = csv.reader(f, delimiter='\t')

            for i in xrange(24):
                next(reader, None)

            for row in reader:
                self.add_go_annotation_to_gene(gene_id=row[1], go_id=row[4])

    def load_diseases(self):
        disease_data_csv_filename = "data/Diseases_OMIM_IDs_and_synonyms_(WormBase).txt"

        print("Fetching disease data from WormBase txt file...")

        with open(disease_data_csv_filename, 'rb') as f:
            reader = csv.reader(f, delimiter='\t')
            next(reader, None)

            for row in reader:
                if row[2] and row[2] != "":
                    omim_ids = map(lambda s: s.strip(), row[2].split(","))

                    for omim_id in omim_ids:
                        self.add_disease_annotation_to_gene(gene_id=None, omim_id="OMIM:"+omim_id)
