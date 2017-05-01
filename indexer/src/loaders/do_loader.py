from files import *
from obo_parser import *
import sys
import re
import pprint

class DoLoader:
    @staticmethod
    def get_data():
        path = "tmp";
        S3File("mod-datadumps", "disease-ontology.obo", path).download()
        do_data = TXTFile(path + "/disease-ontology.obo").get_data()

        do_dataset = {}

        creating_term = None

        for line in do_data:
            line = line.strip()

            if line == "[Term]":
                creating_term = True
            elif line == '': # Skip blank lines
                continue
            elif creating_term:
                key = (line.split(":")[0]).strip()
                value = ("".join(":".join(line.split(":")[1:]))).strip()

                if key == "id":
                    creating_term = value
                    do_dataset[creating_term] = {"id": value}
                else:
                    if key == "synonym":
                        if value.split(" ")[-2] == "EXACT":
                            value = (" ".join(value.split(" ")[:-2]))[1:-1]
                        else:
                            continue
                    if key == "def":
                        m = re.search('\"(.+)\"', value)
                        value = m.group(1)

                    if key in do_dataset[creating_term]:
                        do_dataset[creating_term][key].append(value)
                    else:
                        do_dataset[creating_term][key] = [value]
        return do_dataset
    #
    #
    # @staticmethod
    # def get_data():
    #     path = "tmp";
    #     S3File("mod-datadumps", "disease-ontology.obo", path).download()
    #     parsed_line = parseGOOBO(path + "/disease-ontology.obo")
    #     dict_to_return = {}
    #     for line in parsed_line: # Convert parsed obo term into a schema-friendly AGR dictionary.
    #         do_id = line['id']
    #         dict_to_return[do_id] = {
    #             'do_genes': [],
    #             'do_species': [],
    #             'name': line['name'],
    #             'description': line.get('def'),
    #             #no namespace in diseae-ontology file
    #             'do_type': line.get('namespace'),
    #             'do_synonyms': line.get('synonym'),
    #             'name_key': line['name'],
    #             'id': do_id,
    #             'href': 'http://www.disease-ontology.org/?id=' + line['id'],
    #             'category': 'do'
    #         }
    #     return dict_to_return
