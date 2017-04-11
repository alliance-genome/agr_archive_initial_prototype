from files import *
from obo_parser import *

import re

class DoLoader:


    @staticmethod
    def get_data():
        path = "tmp";
        S3File("mod-datadumps/data", "do.obo", path).download()
        parsed_line = parseGOOBO(path + "/do.obo")
        dict_to_return = {}
        for line in parsed_line: # Convert parsed obo term into a schema-friendly AGR dictionary.
            do_id = line['id']
            dict_to_return[go_id] = {
                'do_genes': [],
                'do_species': [],
                'name': line['name'],
                'description': line['def'],
                'do_type': line['namespace'],
                'do_synonyms': line.get('synonym'),
                'name_key': line['name'],
                'id': do_id,
                'href': 'http://www.disease-ontology.org/?id=' + line['id'],
                'category': 'do'
            }
        return dict_to_return
