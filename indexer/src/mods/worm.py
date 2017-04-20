from mod import MOD
from files import *
from loaders.gene_loader import GeneLoader
from loaders.disease_loader import DiseaseLoader
import gzip
import csv

class WormBase(MOD):
    species = "Caenorhabditis elegans"

    @staticmethod
    def gene_href(gene_id):
        return "http://www.wormbase.org/species/c_elegans/gene/" + gene_id

    @staticmethod
    def get_organism_names():
        return ["Caenorhabditis elegans", "C. elegans", "CAEEL"]

    @staticmethod
    def gene_id_from_panther(panther_id):
        # example: WormBase=WBGene00004831
        return panther_id.split("=")[1]

    def load_genes(self, batch_size, test_set):
        path = "tmp"
        S3File("mod-datadumps", "WB_0.6.1_1.tar.gz", path).download()
        TARFile(path, "WB_0.6.1_1.tar.gz").extract_all()
        gene_data = JSONFile().get_data(path + "/WB_0.6.1_BGI.json")
        gene_lists = GeneLoader().get_data(gene_data, batch_size, test_set)
        for entry in gene_lists:
             yield entry

    def load_go(self):
        path = "tmp"
        S3File("mod-datadumps/GO/ANNOT", "gene_association.wb.gz", path).download()
        go_annot_dict = {}
        with gzip.open(path + "/gene_association.wb.gz", 'rb') as file:
            reader = csv.reader(file, delimiter='\t')
            for line in reader:
                if line[0].startswith('!'):
                    continue
                gene = line[0] + ":" + line[1]
                go_id = line[4]
                if gene in go_annot_dict:
                    go_annot_dict[gene]['go_id'].append(go_id)
                else:
                    go_annot_dict[gene] = {
                        'gene_id': gene,
                        'go_id': [go_id],
                        'species': WormBase.species
                    }
        return go_annot_dict

    def load_diseases(self):
        path = "tmp"
        S3File("mod-datadumps", "WB_0.6.1_1.tar.gz", path).download()
        TARFile(path, "WB_0.6.1_1.tar.gz").extract_all()
        disease_data = JSONFile().get_data(path + "/WB_0.6.1_disease.json")
        gene_disease_dict = DiseaseLoader().get_data(disease_data)

        return gene_disease_dict
