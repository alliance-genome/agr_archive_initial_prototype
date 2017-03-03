from files import *

import re

class GoLoader:

    def __init__(self):
        path = "tmp";
        S3File("mod-datadumps/data", "go.obo", path).download()
        self.go_data = TXTFile(path + "/go.obo").get_data()

    def get_data(self):
        go_dataset = {}
        creating_term = None

        for line in self.go_data:
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
