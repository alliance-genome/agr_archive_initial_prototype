from files import *
from loaders import *
import time
import gc
import json
from test_check import check_for_test_entry

class OrthoLoader:

    @staticmethod
    def get_data(mod_name, test_set):
        path = "tmp"
        filename = "/orthology_" + mod_name + "_0.6.1_2.json"
        filename_comp = "orthology_" + mod_name + "_0.6.1_2.json.tar.gz"
        S3File("mod-datadumps/ORTHO", filename_comp, path).download()
        TARFile(path, filename_comp).extract_all()
        ortho_data = JSONFile().get_data(path + filename)

        ortho_dataset = {}

        dateProduced = ortho_data['metaData']['dateProduced']
        dataProvider = ortho_data['metaData']['dataProvider']
        release = None

        if 'release' in ortho_data['metaData']:
            release = ortho_data['metaData']['release']

        for orthoRecord in ortho_data['data']:
            ortho_entry = {}

            # Sort out identifiers and prefixes.
            gene1 = IdLoader().process_identifiers(orthoRecord['gene1'], dataProvider) # 'DRSC:'' removed, local ID, functions as display ID.
            gene2 = IdLoader().process_identifiers(orthoRecord['gene2'], dataProvider) # 'DRSC:'' removed, local ID, functions as display ID.

            gene1Species = orthoRecord['gene1Species']
            gene2Species = orthoRecord['gene2Species']

            gene1AgrPrimaryId = IdLoader().add_agr_prefix_by_species(gene1, gene1Species) # Prefixed according to AGR prefixes.
            gene2AgrPrimaryId = IdLoader().add_agr_prefix_by_species(gene2, gene2Species) # Prefixed according to AGR prefixes.

            if test_set == 'true': # If we're using a test set, only import info for test_set genes.
                is_it_test_entry = check_for_test_entry(gene1AgrPrimaryId)
                if is_it_test_entry == 'false':
                    continue

            if gene1AgrPrimaryId not in ortho_dataset:
                ortho_dataset[gene1AgrPrimaryId] = []
            ortho_dataset[gene1AgrPrimaryId].append({
                'isBestScore': orthoRecord['isBestScore'],
                'isBestRevScore': orthoRecord['isBestRevScore'],

                'gene1AgrPrimaryId': gene1AgrPrimaryId,
                'gene1DisplayId' : gene1,
                'gene1Species': gene1Species,

                'gene2AgrPrimaryId': gene2AgrPrimaryId,
                'gene2DisplayId' : gene2,
                'gene2Species': gene2Species,

                'predictionMethodsMatched': orthoRecord['predictionMethodsMatched'],
                'predictionMethodsNotMatched': orthoRecord['predictionMethodsNotMatched'],
                'predictionMethodsNotCalled': orthoRecord['predictionMethodsNotCalled'],

                'confidence': orthoRecord['confidence']
            })

        del ortho_data
        return ortho_dataset