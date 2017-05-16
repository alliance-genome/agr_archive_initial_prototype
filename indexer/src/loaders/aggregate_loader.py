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
        self.chunk_size = 5000 # Set size of chunks sent to ES.

    def establish_index(self):
        print "ES_HOST: " + os.environ['ES_HOST']
        print "ES_INDEX: " + os.environ['ES_INDEX']
        print "ES_AWS: " + os.environ['ES_AWS']
        self.es = ESMapping(os.environ['ES_HOST'], os.environ['ES_INDEX'], os.environ['ES_AWS'], self.chunk_size)
        self.es.start_index()

    def load_annotations(self):
        print "Loading GO Data"
        self.go_dataset = GoLoader().get_data()
        print "Loading SO Data"
        self.so_dataset = SoLoader().get_data()
        print "Loading DO Data"
        self.do_dataset = DoLoader().get_data()

    def load_from_mods(self, test_set):
        mods = [RGD(), MGI(), ZFIN(), SGD(), WormBase(), FlyBase(), Human()]

        gene_master_dict = {} # Build a dictionary of sets for all indexed MODs/genes. Used for filtering orthology.

        self.test_set = test_set
        if self.test_set == 'true':
            print "WARNING: test_set is enabled -- only indexing test genes."
            time.sleep(3)

        print "Gathering genes from each MOD."
        for mod in mods:

            gene_master_dict[mod.__class__.__name__] = set()

            genes = mod.load_genes(self.batch_size, self.test_set) # generator object
            print "Loading GO annotations for %s" % (mod.species)
            gene_go_annots = mod.load_go()
            print "Loading DO annotations for %s" % (mod.species)
            disease_annots = mod.load_diseases()

            for gene_list_of_entries in genes:
                # Annotations to individual genes occurs in the loop below via static methods.
                print "Attaching annotations to individual genes."

                for item, individual_gene in enumerate(gene_list_of_entries):
                    # The Do and GoAnnotators also updates their ontology datasets as they annotates genes, hence the two variable assignment.
                    (gene_list_of_entries[item], self.go_dataset) = GoAnnotator().attach_annotations(individual_gene, gene_go_annots, self.go_dataset)
                    gene_list_of_entries[item] = DoAnnotator().attach_annotations(individual_gene, disease_annots, self.do_dataset)
                    gene_list_of_entries[item] = SoAnnotator().attach_annotations(individual_gene, self.so_dataset)
                    gene_master_dict[mod.__class__.__name__].add(individual_gene['primaryId'])

                self.es.index_data(gene_list_of_entries, 'Gene Data', 'index') # Load genes into ES

        print "Processing orthology data for each MOD."
        for mod in mods:

            list_to_index = []

            print "Loading Orthology data for %s" % (mod.species)
            ortho_dataset = OrthoLoader().get_data(mod.__class__.__name__, self.test_set, gene_master_dict[mod.__class__.__name__])

            for gene in gene_master_dict[mod.__class__.__name__]:
                # Create a simple dictionary for each entry.
                individual_gene = {
                    'primaryId' : gene,
                    'orthology' : []
                    }
                individual_gene = OrthoAnnotator().attach_annotations(individual_gene, ortho_dataset)

                list_to_index.append(individual_gene)
                if len(list_to_index) == self.batch_size:
                    self.es.update_data(list_to_index) # Load genes into ES
                    list_to_index[:] = []  # Empty the list.

            if len(list_to_index) > 0:
                self.es.update_data(list_to_index) # Load genes into ES    

    def index_data(self):
        self.es.index_data(self.go_dataset, 'GO Data', 'index') # Load the GO dataset into ES
        self.es.index_data(self.do_dataset, 'DO Data', 'index') # Load the DO dataset into ES
        self.es.finish_index()