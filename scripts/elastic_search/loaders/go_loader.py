from files import *
from obo_parser import *

import re

class GoLoader:

    def use_obo_parser(self):
        path = "tmp";
        S3File("mod-datadumps/data", "go.obo", path).download()
        parsed_line = parseGOOBO(path + "/go.obo")
        list_to_yield = []
        for line in parsed_line: # Convert parsed obo term into a schema-friendly AGR dictionary.
            list_to_yield.append({ # Append anonymous dictionary to list.
                    'name': line['name'],
                    'description': line['def'],
                    'go_type': line['namespace'],
                    'go_synonyms': line.get('synonym'),

                    'name_key': line['name'],
                    'id': line['id'],
                    'href': 'http://amigo.geneontology.org/amigo/term/' + line['id'],
                    'category': 'go'
            })
            if len(list_to_yield) == 5000:
                yield list_to_yield
        if len(list_to_yield) > 0:
            yield list_to_yield

    def process_data(self):

            self.go[go_id] = {
                "go_genes": [gene_symbol],
                "go_species": [species],

                "name": self.go_dataset[go_id]["name"][0],
                "description": self.go_dataset[go_id]["def"][0],
                "go_type": self.go_dataset[go_id]["namespace"][0],
                "go_synonyms": self.go_dataset[go_id].get("synonym"),

                "name_key": self.go_dataset[go_id]["name"][0],
                "id": go_id,
                "href": "http://amigo.geneontology.org/amigo/term/" + go_id,
                "category": "go"
            }

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