from intermine.webservice import Service
from files import *
from loaders.gene_loader import GeneLoader
import csv
import gzip
from loaders.disease_loader import DiseaseLoader
from mod import MOD

class ZFIN(MOD):
    species = "Danio rerio"

    def __init__(self):
        self.service = Service("http://www.zebrafishmine.org/service")

    @staticmethod
    def gene_href(gene_id):
        return "http://zfin.org/" + gene_id

    @staticmethod
    def get_organism_names():
        return ["Danio rerio", "D. rerio", "DANRE"]

    @staticmethod
    def gene_id_from_panther(panther_id):
        # example: ZFIN=ZDB-GENE-010525-1
        return panther_id.split("=")[1]

    def load_genes(self, batch_size, test_set):
        path = "tmp"
        S3File("mod-datadumps", "ZFIN_0.6.0_7.tar.gz", path).download()
        TARFile(path, "ZFIN_0.6.0_7.tar.gz").extract_all()
        gene_data = JSONFile().get_data(path + "/ZFIN_0.6.0_BGI.json")
        gene_lists = GeneLoader().get_data(gene_data, batch_size, test_set)
        for entry in gene_lists:
             yield entry

    def load_go(self):
        path = "tmp"
        S3File("mod-datadumps/GO/ANNOT", "gene_association.zfin.gz", path).download()
        go_annot_dict = {}
        with gzip.open(path + "/gene_association.zfin.gz", 'rb') as file:
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
                        'species': ZFIN.species
                    }
        return go_annot_dict

    def load_disease(self):
        path = "tmp"
        S3File("mod-datadumps", "ZFIN_0.6.0_7.tar.gz", path).download()
        TARFile(path, "ZFIN_0.6.0_7.tar.gz").extract_all()
        disease_data = JSONFile().get_data(path + "/ZFIN_0.6.0_DAF.json")
        gene_disease_dict = DiseaseLoader().get_data(disease_data)

        return gene_disease_dict
