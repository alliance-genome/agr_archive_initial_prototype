from files import *
import time
import gc
import json
from test_check import check_for_test_entry

class OrthoLoader:

    @staticmethod
    def get_data(mod_name, test_set):
        path = "tmp"
        filename = "/orthology_" + mod_name + ".json"
        filename_comp = "orthology_" + mod_name + ".json.tar.gz"
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
            primaryId = orthoRecord['gene1']
            if test_set == 'true':
                is_it_test_entry = check_for_test_entry(primaryId)
                if is_it_test_entry == 'false':
                    continue
            if primaryId not in ortho_dataset:
                ortho_dataset[primaryId] = []
            ortho_dataset[primaryId].append({
                'isBestScore': orthoRecord['isBestScore'],
                'isBestRevScore': orthoRecord['isBestRevScore'],
                'gene1DataProvider': orthoRecord['gene1DataProvider'],
                'gene2': orthoRecord['gene2'],
                'gene2DataProvider': orthoRecord['gene2DataProvider'],
                'predictionMethodsMatched': orthoRecord['predictionMethodsMatched'],
                'predictionMethodsNotMatched': orthoRecord['predictionMethodsNotMatched'],
                'predictionMethodsNotCalled': orthoRecord['predictionMethodsNotCalled'],
                'confidence': orthoRecord['confidence']
            })

        del ortho_data
        return ortho_dataset