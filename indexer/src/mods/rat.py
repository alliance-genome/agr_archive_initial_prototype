from intermine.webservice import Service
from loaders.gene_loader import GeneLoader
from mod import MOD
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

    def load_genes(self):
        path = "tmp"
        S3File("mod-datadumps", "RGD_0.3_1.tar.gz", path).download()
        TARFile(path, "RGD_0.3_1.tar.gz").extract_all()
        return GeneLoader(path + "/agr/RGD_0.3_basicGeneInformation.10116.json").get_data()

    def load_go(self):
        path = "tmp"
        S3File("mod-datadumps/data", "rat_go.tsv", path).download()
        go_data = CSVFile(path + "/rat_go.tsv").get_data()

        list = []
        for row in go_data:
            list.append({"gene_id": row[5], "go_id": row[1], "species": RGD.species})
        return list

    def load_diseases(self):
        path = "tmp"
        S3File("mod-datadumps/data", "rat_disease.tsv", path).download()
        disease_data = CSVFile(path + "/rat_disease.tsv").get_data()

        list = []
        for row in disease_data:
            if (row[5].startswith("OMIM:")):
                list.append({"gene_id": row[0], "omim_id": row[5], "species": RGD.species})
        return list
