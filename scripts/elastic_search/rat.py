from intermine.webservice import Service
from mod import MOD
import csv


class RGD(MOD):
    species = "Rattus norvegicus"
    service = Service("http://ratmine.mcw.edu/ratmine/service")
    path_to_basic_gene_information_file = "data/rat_gene_info.json"

    @staticmethod
    def gene_href(gene_id):
        return "http://www.rgd.mcw.edu/rgdweb/report/gene/main.html?id=" + gene_id

    @staticmethod
    def gene_id_from_panther(panther_id):
        # example: RGD=628644
        return panther_id.replace("=", ":")

    def load_go(self):
        go_data_csv_filename = "data/rat_go.tsv"

        print("Fetching go data from RGD tsv file...")

        with open(go_data_csv_filename, 'rb') as f:
            reader = csv.reader(f, delimiter='\t')

            for row in reader:
                self.add_go_annotation_to_gene(gene_id=row[5], go_id=row[1])

    def load_diseases(self):
        disease_data_csv_filename = "data/rat_disease.tsv"

        print("Fetching disease data from RGD tsv file...")

        with open(disease_data_csv_filename, 'rb') as f:
            reader = csv.reader(f, delimiter='\t')

            for row in reader:
                if (row[5].startswith("OMIM:")):
                    self.add_disease_annotation_to_gene(gene_id=row[0], omim_id=row[5])

    def load_genes(self, path_to_file):
        return super(RGD, self).load_genes(path_to_basic_gene_information_file)
