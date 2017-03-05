from files import *

import re

class OMIMLoader:

    def __init__(self):
        path = "tmp";
        S3File("mod-datadumps/data", "OMIM_diseases.txt", path).download()
        self.omim_data = CSVFile(path + "/OMIM_diseases.txt").get_data()

    def get_data(self):
        omim_dataset = {}

        for row in self.omim_data:
            if len(row) < 3:
                continue

            name_column = row[2].split(";")
            name = name_column[0].strip()
            if len(name_column) > 1:
                symbol = name_column[1].strip()
            else:
                symbol = None

            synonyms = []

            for r in (row[3], row[4]):
                if r == '':
                    continue

                alternative_names = r.split(";;")

                for alt_name_symbol in alternative_names:
                    alt_name_symbol = alt_name_symbol.split(";")
                    alt_name = alt_name_symbol[0].strip().lower()
                    if len(alt_name_symbol) > 1:
                        alt_symbol = ", " + alt_name_symbol[1].strip()
                    else:
                        alt_symbol = ""

                    synonyms.append(alt_name + alt_symbol)

            omim_dataset["OMIM:" + row[1]] = {
                "prefix": row[0],
                "name": name.lower(),
                "symbol": symbol,
                "disease_synonyms": synonyms
            }

        return omim_dataset
