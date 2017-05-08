from mod import MOD
from files import *
from loaders.gene_loader import GeneLoader
from loaders.disease_loader import DiseaseLoader
import gzip
import csv
from BCBio import GFF
from BCBio.GFF import GFFExaminer
import pprint


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

    def load_gff(self):
        path = "tmp"
        filename = "c_elegans.PRJNA13758.WS258.genes_only.gff3"
        filenameCompressed = "c_elegans.PRJNA13758.WS258.genes_only.gff3.tar.gz"
        S3File("mod-datadumps/gff3", filenameCompressed, path).download()
        TARFile(path, filenameCompressed).extract_all

        # GFF3 Parsing

        gene_dict = {}
        mRNA_dict = {}

        examiner = GFF.GFFExaminer()
        with open(path + '/' + filename) as gff_handle:
            possible_limits = examiner.available_limits(gff_handle)
        chromosomes = sorted(possible_limits["gff_id"].keys())
        types = sorted(possible_limits["gff_type"].keys())
        limits = dict(gff_type = [('gene',), ('mRNA',), ('CDS',)])
        for chrom in chromosomes:
            with open(path + '/' + filename) as gff_handle:
                limits["gff_id"] = chrom
                print "Processing GFF with limits: %s" % (limits)
                for rec in GFF.parse(gff_handle, limit_info = limits, target_lines=1):
                    for feature in rec.features:
                        # print feature.type
                        if feature.type == 'gene':
                            feature_id = 'WB:' + feature.qualifiers['ID'][0].split(":",1).pop()
                            if feature_id not in gene_dict:
                                gene_dict[feature_id] = {}
                        elif feature.type == 'mRNA':
                            feature_parent = 'WB:' + feature.qualifiers['Parent'][0].split(":",1).pop()
                            feature_id = feature.qualifiers['ID'][0]
                            feature_location = {
                                'startPosition' : feature.location.start,
                                'endPosition' : feature.location.end,
                                'strand' : feature.location.strand
                            }
                            if feature_id not in gene_dict[feature_parent]:
                                gene_dict[feature_parent][feature_id] = {}
                                mRNA_dict[feature_id] = {}
                            gene_dict[feature_parent][feature_id]['location'] = feature_location

                        elif feature.type == 'CDS':
                            feature_parent = feature.qualifiers['Parent'][0]
                            feature_id = feature.qualifiers['ID'][0]
                            feature_location = {
                                'startPosition' : feature.location.start,
                                'endPosition' : feature.location.end,
                                'strand' : feature.location.strand
                            }

                            if feature_id not in mRNA_dict[feature_parent]:
                                mRNA_dict[feature_parent][feature_id] = {}
                                mRNA_dict[feature_parent][feature_id]['locations'] = []
                            mRNA_dict[feature_parent][feature_id]['locations'].append(feature_location)

        for genes in gene_dict: # Update the gene_dict with mRNA_dict
            for mRNA in gene_dict[genes]:
                gene_dict[genes][mRNA].update(mRNA_dict[mRNA])

        return gene_dict