from intermine.webservice import Service
from loaders.gene_loader import GeneLoader
from mod import MOD
import gzip
import csv
from files import *

class RGD(MOD):
    species = "Rattus norvegicus"
    service = Service("http://ratmine.mcw.edu/ratmine/service")

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
        S3File("mod-datadumps", "RGD_0.3_1.tar.gz", path).download()
        TARFile(path, "RGD_0.3_1.tar.gz").extract_all()
        gene_data = JSONFile().get_data(path + "/agr/RGD_0.3_basicGeneInformation.10116.json")
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
                if gene in go_annot_dict:
                    go_annot_dict[gene]['go_id'].append(go_id)
                else:
                    go_annot_dict[gene] = {
                        'gene_id': gene,
                        'go_id': [go_id],
                        'species': RGD.species
                    }
        return go_annot_dict

    def load_diseases(self):
        path = "tmp"
        S3File("mod-datadumps/data", "rat_disease.tsv", path).download()
        disease_data = CSVFile(path + "/rat_disease.tsv").get_data()

        list = []
        for row in disease_data:
            if (row[5].startswith("OMIM:")):
                list.append({"gene_id": row[0], "omim_id": row[5], "species": RGD.species})
        return list
