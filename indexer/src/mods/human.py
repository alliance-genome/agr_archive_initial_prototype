from mod import MOD
from loaders.gene_loader import GeneLoader
from loaders.disease_loader import DiseaseLoader
import gzip
import csv
from files import *

class Human(MOD):
    species = "Homo sapiens"

    @staticmethod
    def gene_href(gene_id):
        return "http://www.genenames.org/cgi-bin/gene_symbol_report?hgnc_id=" + gene_id

    @staticmethod
    def get_organism_names():
        return ["Homo sapiens", "H. sapiens", "HUMAN"]

    @staticmethod
    def gene_id_from_panther(panther_id):
        # example: HGNC=974
        return panther_id.replace("=", ":")

    def load_genes(self, batch_size, test_set):
        path = "tmp"
        S3File("mod-datadumps", "RGD_0.6_1.tar.gz", path).download()
        TARFile(path, "RGD_0.6_1.tar.gz").extract_all()
        gene_data = JSONFile().get_data(path + "/RGD_0.6.2_basicGeneInformation.9606.json")
        gene_lists = GeneLoader().get_data(gene_data, batch_size, test_set)
        for entry in gene_lists:
             yield entry

    def load_go(self):
        path = "tmp"
        S3File("mod-datadumps/GO/ANNOT", "gene_association.human.gz", path).download()
        go_annot_dict = {}
        with gzip.open(path + "/gene_association.human.gz", 'rb') as file:
            reader = csv.reader(file, delimiter='\t')
            for row in reader:
                gene = row[0]
                go_terms = map(lambda s: s.strip(), row[1].split(","))
                for term in go_terms:
                    if gene in go_annot_dict:
                        go_annot_dict[gene]['go_id'].append(term)
                    else:
                        go_annot_dict[gene] = {
                            'gene_id': gene,
                            'go_id': [term],
                            'species': Human.species
                        }
        return go_annot_dict

    def load_diseases(self):

        path = "tmp"
        S3File("mod-datadumps", "RGD_0.6.2.tar.gz", path).download()
        TARFile(path, "RGD_0.6.2.tar.gz").extract_all()
        disease_data = JSONFile().get_data(path + "/RGD_0.6.2_disease.9606.daf.json")
        gene_disease_dict = DiseaseLoader().get_data(disease_data)

        return gene_disease_dict