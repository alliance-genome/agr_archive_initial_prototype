from files import *
from obo_parser import *

import re

class SoLoader:

    @staticmethod
    def get_data():
        path = "tmp";
        S3File("mod-datadumps/data", "so.obo", path).download()
        parsed_line = parseGOOBO(path + "/so.obo")
        dict_to_return = {}
        for line in parsed_line: # Convert parsed obo term into a schema-friendly AGR dictionary.
            go_id = line['id']
            dict_to_return[go_id] = {
                'name': line['name']
            }
        return dict_to_return