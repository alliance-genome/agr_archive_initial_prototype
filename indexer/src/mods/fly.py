from loaders.gene_loader import GeneLoader
from mod import MOD
from files import *
import gzip
import csv

class FlyBase(MOD):
    species = "Drosophila melanogaster"

    @staticmethod
    def gene_href(gene_id):
        return "http://flybase.org/reports/" + gene_id + ".html"

    @staticmethod
    def get_organism_names():
        return ["Drosophila melanogaster", "D. melanogaster", "DROME"]

    def load_genes(self, batch_size, test_set):
        path = "tmp"
        S3File("mod-datadumps", "FB_0.3.0_1.tar.gz", path).download()
        TARFile(path, "FB_0.3.0_1.tar.gz").extract_all()
        gene_data = JSONFile().get_data(path + "/FB_0.3_basicGeneInformation.json")
        gene_lists = GeneLoader().get_data(gene_data, batch_size, test_set)
        for entry in gene_lists:
             yield entry

    @staticmethod
    def gene_id_from_panther(panther_id):
        # example: FlyBase=FBgn0053056
        return panther_id.split("=")[1]

    def load_go(self):
        path = "tmp"
        S3File("mod-datadumps/GO/ANNOT", "gene_association.fb.gz", path).download()
        go_annot_dict = {}
        with gzip.open(path + "/gene_association.fb.gz", 'rb') as file:
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
                        'species': FlyBase.species
                    }
        return go_annot_dict

    def load_disease(self):
        list = []
        return list

