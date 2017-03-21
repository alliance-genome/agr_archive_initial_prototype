from mapping import ESMapping
from loaders import *
from files import *
from mods import *

import os

class AggregateLoader:

    def load_from_mods(self):
        #mods = [RGD(), MGI(), ZFIN(), SGD(), WormBase(), FlyBase(), Human()]
        mods = [FlyBase(), WormBase()]

        print "Loading GO Data"
        go_data = GoLoader().get_data() 
        print "Loading OMIM Data"
        omim_data = OMIMLoader().get_data()
        print "Loading SO Data"
        so_loader = SoLoader()

        self.gene_master_list = [] # Master list of gene IDs across all MODs
        print "Gathering genes from Each Mod"
        for mod in mods:
            self.genes = {}
            self.genes.update(mod.load_genes())
            self.gene_master_list.extend(self.genes.keys()) # keys() returns a list so we extend, rather than append
            self.es.index_data(self.genes, "Gene Data")

        # # print "Loading Homologs for all genes"
        # # HomoLogLoader(mods).attach_homolog_data(genes)
        # print "Loading SO terms for all genes"
        # so_loader.attach_so_data(self.genes)

        # print "Loading GO annotations for genes from mines"
        # gene_go_annots = []
        # # gene_disease_annots = []
        # for mod in mods:
        #     gene_go_annots.extend(mod.load_go())
        #     # gene_disease_annots.extend(mod.load_diseases())

        # print "Attaching GO annotations to genes"
        # go_annot_loader = GoGeneAnnotLoader(self.genes, go_data)
        # self.go_entries = go_annot_loader.attach_annotations(gene_go_annots)

        # # print "Attaching Disease annotations to genes"
        # # disease_annot_loader = DiseaseGeneAnnotLoader(genes, omim_data)
        # # disease_entries = disease_annot_loader.attach_annotations(gene_disease_annots)

    def load_from_files(self):
        print "Load data from saved files"
        self.genes = PickleFile("tmp/genes_bkp.pickle").load()
        self.go_entries = PickleFile("tmp/go_bkp.pickle").load()
        #so_entries = PickleFile("tmp/so_bkp.pickle").load()
        #disease_entries = PickleFile("tmp/diseases_bkp.pickle").load()

    def save_to_files(self):
        print "Saving processed data to files"
        PickleFile("tmp/genes_bkp.pickle").save(self.genes)
        # PickleFile("tmp/go_bkp.pickle").save(self.go_entries)
        # PickleFile("tmp/diseases_bkp.pickle").save(disease_entries)
        # PickleFile("tmp/so_bkp.pickle").save(so_loader.get_data())

    def establish_index(self):
        self.es = ESMapping(os.environ['ES_HOST'], os.environ['ES_INDEX'], os.environ['ES_AWS'])
        self.es.start_index()

    def index_data(self):
        # self.es.index_data(self.go_entries, "Go Data")
        # self.index_into_es(disease_entries)
        self.es.finish_index()