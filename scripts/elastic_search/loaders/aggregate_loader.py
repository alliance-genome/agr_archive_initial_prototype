from mapping import ESMapping
from loaders import *
from annotators import *
from files import *
from mods import *
import memory_profiler
import psutil
import gc

import os

class AggregateLoader:

    @profile
    def load_from_mods(self):
        #mods = [RGD(), MGI(), ZFIN(), SGD(), WormBase(), FlyBase(), Human()]
        mods = [FlyBase(), WormBase()]

        print "Loading GO Data"
        go_loader = GoLoader().use_obo_parser()
        for line in go_loader:
            print line
        #go_dataset = go_loader.get_data()
        print "Loading OMIM Data"
        omim_data = OMIMLoader().get_data()
        print "Loading SO Data"
        so_loader = SoLoader()
        so_dataset = so_loader.get_data()

        self.gene_master_list = [] # Master list of gene IDs across all MODs.

        print "Gathering genes from Each Mod"
        for mod in mods:
            genes = mod.load_genes()

            print "Attaching SO terms."
            genes = SoAnnotator().attach_annotations(genes, so_dataset)
            
            self.es.index_data(genes, 'Gene Data', 'index') # Use 'index' for the initial gene indexing.

            print "Loading GO annotations from mines or files."
            gene_go_annots = mod.load_go()

            print "Attaching GO annotations to genes."
            genes = GoAnnotator().attach_annotations(genes, gene_go_annots, go_dataset)
            
            self.gene_master_list.extend(gene_list)

            # print gene_list
            # gene_list = genes.keys() # Create a new list with only the keys from self.genes.
            # genes.clear() # Remove the genes dictionary.

    def load_from_files(self):
        print "Load data from saved files"
        self.genes = PickleFile("tmp/genes_bkp.pickle").load()
        self.go_entries = PickleFile("tmp/go_bkp.pickle").load()
        #so_entries = PickleFile("tmp/so_bkp.pickle").load()
        #disease_entries = PickleFile("tmp/diseases_bkp.pickle").load()

    def save_to_files(self):
         print "Saving processed data to files"
        # PickleFile("tmp/genes_bkp.pickle").save(self.genes)
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