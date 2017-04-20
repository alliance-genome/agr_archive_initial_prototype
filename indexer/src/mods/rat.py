from loaders.gene_loader import GeneLoader
from loaders.disease_loader import DiseaseLoader
from mod import MOD
import gzip
import csv
from files import *

class RGD(MOD):
    species = "Rattus norvegicus"

    @staticmethod
    def gene_href(gene_id):
        return "http://www.rgd.mcw.edu/rgdweb/report/gene/main.html?id=" + gene_id

    @staticmethod
    def get_organism_names():
        return ["Rattus norvegicus", "R. norvegicus", "RAT"]

    @staticmethod
    def gene_id_from_panther(panther_id):
        # example: RGD=628644
        return panther_id.replace("=", ":")

    def load_genes(self, batch_size, test_set):
        path = "tmp"
        S3File("mod-datadumps", "RGD_0.6_1.tar.gz", path).download()
        TARFile(path, "RGD_0.6_1.tar.gz").extract_all()
        gene_data = JSONFile().get_data(path + "/RGD_0.6_basicGeneInformation.10116.json")
        gene_lists = GeneLoader().get_data(gene_data, batch_size, test_set)
        for entry in gene_lists:
             yield entry

    def load_go(self):
        path = "tmp"
        S3File("mod-datadumps/GO/ANNOT", "gene_association.rgd.gz", path).download()
        go_annot_dict = {}
        with gzip.open(path + "/gene_association.rgd.gz", 'rb') as file:
            reader = csv.reader(file, delimiter='\t')
            for line in reader:
                if line[0].startswith('!'):
                    continue
                gene = line[1]
                go_id = line[4]
                prefix = line[0]
                if gene in go_annot_dict:
                    go_annot_dict[gene]['go_id'].append(go_id)
                else:
                    go_annot_dict[gene] = {
                        'gene_id': gene,
                        'go_id': [go_id],
                        'species': RGD.species,
                        'prefix':prefix
                    }
        return go_annot_dict

    def load_diseases(self):
        path = "tmp"
        S3File("mod-datadumps", "RGD_0.6_1.tar.gz", path).download()
        TARFile(path, "RGD_0.6_1.tar.gz").extract_all()
        disease_data = JSONFile().get_data(path + "/RGD_0.6_disease.10116.daf.json")
        gene_disease_dict = DiseaseLoader().get_data(disease_data)

        return gene_disease_dict