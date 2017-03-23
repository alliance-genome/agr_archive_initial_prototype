from files import *

import re

class GoLoader:

    def __init__(self):
        self.path = "tmp";
        S3File("mod-datadumps/data", "go.obo", self.path).download()

    def get_data(self):
        go_data = TXTFile(self.path + "/go.obo").get_GO_data()

        for line in go_data:
            creating_term = None
            go_dataset = {}
            line = line.strip()

            if line == "[Term]":
                creating_term = True
            elif creating_term:
                key = (line.split(":")[0]).strip()
                value = ("".join(":".join(line.split(":")[1:]))).strip()

                if key == "id":
                    creating_term = value
                    go_dataset[creating_term] = {}
                else:
                    if key == "synonym":
                        if value.split(" ")[-2] == "EXACT":
                            value = (" ".join(value.split(" ")[:-2]))[1:-1]
                        else:
                            continue
                    if key == "def":
                        m = re.search('\"(.+)\"', value)
                        value = m.group(1)

                    if key in go_dataset[creating_term]:
                        go_dataset[creating_term][key].append(value)
                    else:
                        go_dataset[creating_term][key] = [value]
        return go_dataset

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