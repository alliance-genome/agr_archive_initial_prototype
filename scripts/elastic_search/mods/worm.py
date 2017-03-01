from mod import MOD
from files import *
from loaders.gene_loader import GeneLoader
import xlrd
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

    def load_genes(self):
        path = "tmp"
        S3File("mod-datadumps", "WB_0.3.0_2.tar.gz", path).download()
        TARFile(path, "WB_0.3.0_2.tar.gz").extract_all()
        return GeneLoader(path + "/WB_0.3_basicgeneinformation.json").get_data()

    def load_go(self):
        path = "tmp"
        S3File("mod-datadumps/data", "wormbase_gene_association.tsv", path).download()

        go_data_csv_filename = path + "/wormbase_gene_association.tsv"

        print("Fetching go data from WormBase txt file (" + go_data_csv_filename + ") ...")

        list = []
        with open(go_data_csv_filename, 'rb') as f:
            reader = csv.reader(f, delimiter='\t')

            for i in xrange(24):
                next(reader, None)

            for row in reader:
                list.append({"gene_id": row[1], "go_id": row[4], "species": WormBase.species})
        return list

    def load_diseases(self):
        path = "tmp"
        disease_data_csv_filename = path = "/Diseases_OMIM_IDs_and_synonyms_(WormBase).txt"
        S3File("mod-datadumps/data", "Diseases_OMIM_IDs_and_synonyms_(WormBase).txt", path).download()

        print("Fetching disease data from WormBase txt file (" + disease_data_csv_filename + ") ...")
        list = []
        with open(disease_data_csv_filename, 'rb') as f:
            reader = csv.reader(f, delimiter='\t')
            next(reader, None)

            for row in reader:
                if row[2] and row[2] != "":
                    omim_ids = map(lambda s: s.strip(), row[2].split(","))

                    for omim_id in omim_ids:
                        list.append({"gene_id": None, "omim_id": "OMIM:"+omim_id, "species": WormBase.species})
        return list
