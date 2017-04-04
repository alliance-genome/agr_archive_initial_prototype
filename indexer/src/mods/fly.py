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

    def load_diseases(self):
        path = "tmp"
        S3File("mod-datadumps", "FlyBase_DOID_output_fb_2016_05.tsv", path).download()
        diseases_data_csv_filename = (path + "/FlyBase_DOID_output_fb_2016_05.tsv")

        print("Fetching disease data from FlyBase tsv file (" + diseases_data_csv_filename + ") ...")

        with open(diseases_data_csv_filename, 'rb') as f:
            reader = csv.reader(f, delimiter='\t')
            next(reader, None)

            list = []
            for row in reader:
                if row[3]:
                    omim_ids = map(lambda s: s.strip(), row[3].split(","))
                    disease_gene_ids = map(lambda s: s.strip(), row[5].split(","))

                    for omim_id in omim_ids:
                        for gene_id in disease_gene_ids:
                            list.append({"gene_id": gene_id, "omim_id": "OMIM:"+omim_id, "species": FlyBase.species})
            return list

