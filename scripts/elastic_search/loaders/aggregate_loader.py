from mapping import ESMapping
from loaders import *
from annotators import *
from files import *
from mods import *
import gc

import os

class AggregateLoader:

    def load_from_mods(self):
        mods = [RGD(), MGI(), ZFIN(), SGD(), WormBase(), FlyBase(), Human()]
        #mods = [RGD()]

        print "Loading GO Data"
        go_dataset = GoLoader().get_data()
        print "Loading SO Data" 
        so_dataset = SoLoader().get_data()

        print "Gathering genes from each MOD"
        for mod in mods:
            genes = mod.load_genes() # generator object
            print "Loading GO annotations for %s" % (mod.species)
            gene_go_annots = mod.load_go()

            for gene_list_of_entries in genes:
                # Annotations to individual genes occurs in the loop below.
                print "Attaching annotations to individual genes."
                for individual_gene in gene_list_of_entries:
                    GoAnnotator().attach_annotations(individual_gene, gene_go_annots, go_dataset)
                    SoAnnotator().attach_annotations(individual_gene, so_dataset)
                self.es.index_data(gene_list_of_entries, 'Gene Data', 'index') # Load genes into ES

        self.es.index_data(go_dataset, 'GO Data', 'index') # Load the GO dataset into ES

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