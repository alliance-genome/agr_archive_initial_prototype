from mod import MOD
import xlrd
import csv


class WormBase(MOD):
    species = "Caenorhabditis elegans"
    path_to_basic_gene_information_file = "data/worm_gene_info.json"

    @staticmethod
    def gene_href(gene_id):
        return "http://www.wormbase.org/species/c_elegans/gene/" + gene_id

    @staticmethod
    def gene_id_from_panther(panther_id):
        # example: WormBase=WBGene00004831
        return panther_id.split("=")[1]

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

    def load_genes(self, path_to_file):
        return super(WormBase, self).load_genes(path_to_basic_gene_information_file)
