from mod import MOD
from files import *
from loaders.gene_loader import GeneLoader
import gzip
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

    def load_genes(self, batch_size, test_set):
        path = "tmp"
        S3File("mod-datadumps", "WB_0.3.0_2.tar.gz", path).download()
        TARFile(path, "WB_0.3.0_2.tar.gz").extract_all()
        gene_data = JSONFile().get_data(path + "/WB_0.3_basicgeneinformation.json")
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
                gene = line[1]
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
