from files import *
from loaders import *
from mods import *

import requests
import os
from elasticsearch import Elasticsearch

class FetchAndSave:
    gene_bkp_filename = "tmp/genes_bkp.pickle"
    go_bkp_filename = "tmp/go_bkp.pickle"
    so_bkp_filename = "tmp/so_bkp.pickle"
    # diseases_bkp_filename = "data/diseases_bkp.pickle"

    def load_data_from_sources(self):
        mods = [RGD(), MGI(), ZFIN(), SGD(), WormBase(), FlyBase(), Human()]

        print "Loading Go Data"
        go_data = GoLoader().get_data() 
        print "Loading OMIM Data"
        omim_data = OMIMLoader().get_data()
        print "Loading SO Data"
        so_loader = SoLoader()

        genes = {}
        print "Gathering genes from Each Mod"
        for mod in mods:
            genes.update(mod.load_genes())

        # print "Loading Homologs for all genes"
        # HomoLogLoader(mods).attach_homolog_data(genes)
        print "Loading SO terms for all genes"
        so_loader.attach_so_data(genes)

        print "Loading GO annotations for genes from mines"
        gene_go_annots = []
        # gene_disease_annots = []
        for mod in mods:
            gene_go_annots.extend(mod.load_go())
            # gene_disease_annots.extend(mod.load_diseases())

        print "Attaching GO annotations to genes"
        go_annot_loader = GoGeneAnnotLoader(genes, go_data)
        go_entries = go_annot_loader.attach_annotations(gene_go_annots)

        # print "Attaching Disease annotations to genes"
        # disease_annot_loader = DiseaseGeneAnnotLoader(genes, omim_data)
        # disease_entries = disease_annot_loader.attach_annotations(gene_disease_annots)
        
        print "Saving processed data to files"
        PickleFile(self.gene_bkp_filename).save(genes)
        PickleFile(self.go_bkp_filename).save(go_entries)
        # PickleFile(self.diseases_bkp_filename).save(disease_entries)
        PickleFile(self.so_bkp_filename).save(so_loader.get_data())

if __name__ == '__main__':
    fetch_and_save = FetchAndSave()
    fetch_and_save.load_data_from_sources()
