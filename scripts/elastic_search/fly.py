from mod import MOD
import csv


class FlyBase(MOD):
    species = "Mus musculus"

    @staticmethod
    def gene_href(gene_id):
        return "http://flybase.org/reports/" + gene_id + ".html"

    @staticmethod
    def gene_id_from_panther(panther_id):
        # example: FlyBase=FBgn0053056
        return panther_id.split("=")[1]

    def load_genes(self):
        genes = MOD.genes

        genes_data_csv_filename = "data/FlyBase_Genes_output_fb_2016_04.tsv"

        print("Fetching gene data from FlyBase tsv file...")

        with open(genes_data_csv_filename, 'rb') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                chromosomes = []
                if row[5]:
                    chromosomes = [row[5]]

                genes[row[0]] = {
                    "gene_symbol": row[1],
                    "name": row[1],
                    "description": row[4],
                    "gene_synonyms": map(lambda s: s.strip(), row[9].split(",")),
                    "gene_type": row[3],
                    "gene_chromosomes": chromosomes,
                    "gene_chromosome_starts": row[6],
                    "gene_chromosome_ends": row[7],
                    "gene_chromosome_strand": row[8],
                    "external_ids": [],
                    "species": "Drosophila melanogaster",

                    "gene_biological_process": [],
                    "gene_molecular_function": [],
                    "gene_cellular_component": [],

                    "homologs": [],

                    "name_key": row[1].lower(),
                    "id": row[0],
                    "href": FlyBase.gene_href(row[0]),
                    "category": "gene"
                }

    def load_go(self):
        go_data_csv_filename = "data/FlyBase_GO_output_fb_2016_04.tsv"

        print("Fetching go data from FlyBase tsv file...")

        with open(go_data_csv_filename, 'rb') as f:
            reader = csv.reader(f, delimiter='\t')

            for row in reader:
                go_genes = map(lambda s: s.strip(), row[4].split(","))
                for gene in go_genes:
                    self.add_go_annotation_to_gene(gene_id=gene, go_id='GO:' + row[2])

    def load_diseases(self):
        diseases_data_csv_filename = "data/FlyBase_DOID_output_fb_2016_04.tsv"

        print("Fetching disease data from FlyBase tsv file...")

        with open(diseases_data_csv_filename, 'rb') as f:
            reader = csv.reader(f, delimiter='\t')
            next(reader, None)

            for row in reader:
                if row[3]:
                    omim_ids = map(lambda s: s.strip(), row[3].split(","))
                    disease_gene_ids = map(lambda s: s.strip(), row[5].split(","))

                    for omim_id in omim_ids:
                        for gene_id in disease_gene_ids:
                            self.add_disease_annotation_to_gene(gene_id=gene_id, omim_id="OMIM:"+omim_id)
