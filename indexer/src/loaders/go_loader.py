from files import *
from obo_parser import *

import re

class GoLoader:


    @staticmethod
    def get_data():
        path = "tmp";
        S3File("mod-datadumps/data", "go.obo", path).download()
        parsed_line = parseGOOBO(path + "/go.obo")
        dict_to_return = {}
        for line in parsed_line: # Convert parsed obo term into a schema-friendly AGR dictionary.
            go_id = line['id']
            dict_to_return[go_id] = {
                'go_genes': [],
                'go_species': [],
                'name': line['name'],
                'description': line['def'],
                'go_type': line['namespace'],
                'go_synonyms': line.get('synonym'),

                'name_key': line['name'],
                'id': go_id,
                'href': 'http://amigo.geneontology.org/amigo/term/' + line['id'],
                'category': 'go'
            }

        return dict_to_return
