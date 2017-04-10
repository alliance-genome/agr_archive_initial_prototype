from loaders.gene_loader import GeneLoader
from intermine.webservice import Service
import gzip
import csv
from files import *
from mod import MOD


class SGD(MOD):
    species = "Saccharomyces cerevisiae"

    def __init__(self):
        self.service = Service("http://yeastmine.yeastgenome.org/yeastmine/service")

    @staticmethod
    def gene_href(gene_id):
        return "http://www.yeastgenome.org/locus/" + gene_id + "/overview"

    @staticmethod
    def get_organism_names():
        return ["Saccharomyces cerevisiae", "S. cerevisiae", "YEAST"]

    @staticmethod
    def gene_id_from_panther(panther_id):
        # example: SGD=S000000226
        return panther_id.split("=")[1]

    def load_genes(self, batch_size, test_set):
        path = "tmp"
        S3File("mod-datadumps", "SGD_0.3.0_1.tar.gz", path).download()
        TARFile(path, "SGD_0.3.0_1.tar.gz").extract_all()
        gene_data = JSONFile().get_data(path + "/SGD_0.3_basicGeneInformation.json")
        gene_lists = GeneLoader().get_data(gene_data, batch_size, test_set)
        for entry in gene_lists:
             yield entry

    def load_go(self):
        path = "tmp"
        S3File("mod-datadumps/GO/ANNOT", "gene_association.sgd.gz", path).download()
        go_annot_dict = {}
        with gzip.open(path + "/gene_association.sgd.gz", 'rb') as file:
            reader = csv.reader(file, delimiter='\t')
            for line in reader:
                if line[0].startswith('!'):
                    continue
                gene = line[1]
                go_id = line[4]
                if gene in go_annot_dict:
                    go_annot_dict[gene]['go_id'].append(go_id)
                else:
                    go_annot_dict[gene] = {
                        'gene_id': gene,
                        'go_id': [go_id],
                        'species': SGD.species
                    }
        return go_annot_dict

    def load_disease(self):
        list = []
        return list
