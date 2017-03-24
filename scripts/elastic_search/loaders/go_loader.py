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


    # def process_go_data():
    #     if species == "Danio rerio":
    #         gene_symbol = self.genes[gene_id]["symbol"]
    #     else:
    #         gene_symbol = self.genes[gene_id]["symbol"].upper()   

    #     if go_id in self.go:
    #         if gene_symbol not in self.go[go_id]["go_genes"]:
    #             self.go[go_id]["go_genes"].append(gene_symbol)
    #         if species not in self.go[go_id]["go_species"]:
    #             self.go[go_id]["go_species"].append(species)
    #     else: