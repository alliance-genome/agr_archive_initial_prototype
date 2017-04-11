from mapping import ESMapping
from loaders import *
from annotators import *
from files import *
from mods import *
import gc
import time

import os

class AggregateLoader:

    def __init__(self):
        self.go_dataset = {}
        self.so_dataset = {}
        self.batch_size = 5000 # Set size of gene batches created from JSON file.
        self.chunk_size = 800 # Set size of chunks sent to ES.

    def establish_index(self):
        print "ES_HOST: " + os.environ['ES_HOST']
        print "ES_INDEX: " + os.environ['ES_INDEX']
        print "ES_AWS: " + os.environ['ES_AWS']
        self.es = ESMapping(os.environ['ES_HOST'], os.environ['ES_INDEX'], os.environ['ES_AWS'], self.chunk_size)
        self.es.start_index()

    def load_from_files(self):
        print "Loading data from saved files"
        self.go_dataset = PickleFile("tmp/go_bkp.pickle").load()
        self.so_dataset = PickleFile("tmp/so_bkp.pickle").load()

    def load_annotations(self):
        print "Loading GO Data"
        self.go_dataset = GoLoader().get_data()
        print "Loading SO Data" 
        self.so_dataset = SoLoader().get_data()

    def load_from_mods(self, pickle, index, test_set):
        mods = [RGD(), MGI(), ZFIN(), SGD(), WormBase(), FlyBase(), Human()]

        self.test_set = test_set
        if self.test_set == 'true':
            print "WARNING: test_set is enabled -- only indexing test genes."
            time.sleep(3)

        print "Gathering genes from each MOD"
        for mod in mods:

            pickle_file_name = "tmp/genes_bkp_%s.pickle" % (mod.__class__.__name__)
            if pickle == 'save':
                try:
                    print "Removing %s if it exists." % (pickle_file_name)
                    os.remove(pickle_file_name)
                except OSError:
                    pass

            genes = mod.load_genes(self.batch_size, self.test_set) # generator object
            print "Loading GO annotations for %s" % (mod.species)
            gene_go_annots = mod.load_go()

            print "Loading Orthology data for %s" % (mod.species)
            ortho_dataset = OrthoLoader().get_data(mod.__class__.__name__, self.test_set)

            for gene_list_of_entries in genes:
                # Annotations to individual genes occurs in the loop below via static methods.
                print "Attaching annotations to individual genes."
                
                for item, individual_gene in enumerate(gene_list_of_entries):
                    # The GoAnnotator also updates the go_dataset as it annotates genes, hence the two variable assignment.
                    (gene_list_of_entries[item], self.go_dataset) = GoAnnotator().attach_annotations(individual_gene, gene_go_annots, self.go_dataset)
                    gene_list_of_entries[item] = SoAnnotator().attach_annotations(individual_gene, self.so_dataset)
                    gene_list_of_entries[item] = OrthoAnnotator().attach_annotations(individual_gene, ortho_dataset)

                if pickle == 'save':
                    PickleFile(pickle_file_name).save_append(gene_list_of_entries)

                if index == 'true':
                    self.es.index_data(gene_list_of_entries, 'Gene Data', 'index') # Load genes into ES
                
    def index_mods_from_pickle(self):
        mods = [RGD(), MGI(), ZFIN(), SGD(), WormBase(), FlyBase(), Human()]

        for mod in mods:
            list_to_load = []
            pickle_file_name = "tmp/genes_bkp_%s.pickle" % (mod.__class__.__name__)
            gene_pickle = PickleFile(pickle_file_name).load_multi() # generator object

            for gene in gene_pickle:
                self.es.index_data(list_to_load, 'Gene Data', 'index') # Load genes into ES

    def save_to_files(self):
        print "Saving processed data to files"
        PickleFile("tmp/go_bkp.pickle").save(self.go_dataset)
        PickleFile("tmp/so_bkp.pickle").save(self.so_dataset)

    def index_data(self):
        self.es.index_data(self.go_dataset, 'GO Data', 'index') # Load the GO dataset into ES
        self.es.finish_index()
