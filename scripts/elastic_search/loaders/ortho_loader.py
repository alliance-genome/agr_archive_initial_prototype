from files import *

class OrthoLoader:

    @staticmethod
    def get_data(mod_name):
        path = "tmp"
        filename = "/orthology_" + mod_name + ".json"
        filename_comp = "orthology_" + mod_name + ".json.gz"
        S3File("mod-datadumps/ORTHO", filename_comp, path).download()
        ortho_data = JSONFile().get_data(path + filename)

        ortho_dataset = {}

        dateProduced = ortho_data['metaData']['dateProduced']
        dataProvider = ortho_data['metaData']['dataProvider']
        release = None

        if 'release' in ortho_data['metaData']:
            release = ortho_data['metaData']['release']

        