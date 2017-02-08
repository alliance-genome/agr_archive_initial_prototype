import json
import argparse
import pprint
import sys
from mod import MOD

parser = argparse.ArgumentParser(description='Test loader for JSON basic gene info file.')

parser.add_argument('-d', '--data', help='JSON data file', required=True)
args = parser.parse_args()

# def load_genes(self):
genes = MOD.genes

data_file_name = args.data
with open(data_file_name) as data_file:
    data_content = json.load(data_file)
    #       print data_content['data'][0]['primaryId']
    for geneRecord in data_content['data']:
        crossReferences = []
        for synonym in geneRecord['synonyms']:
            crossReferences.append(synonym)

        genes[geneRecord['primaryId']] = {
            "gene_symbol": geneRecord['symbol'],
            "name": geneRecord['name'],
            # "description": geneRecord['description'],
            "gene_synonyms": crossReferences,
            "gene_type": geneRecord['soTermId'],
            # "gene_chromosomes": chromosomes,
            # "gene_chromosome_starts": row[6],
            # "gene_chromosome_ends": row[7],
            # "gene_chromosome_strand": row[8],
            # "external_ids": [],
            "taxonId": geneRecord['taxonID'],
            # "species": "Drosophila melanogaster",

            # "gene_biological_process": [],
            # "gene_molecular_function": [],
            # "gene_cellular_component": [],

            # "homologs": [],

            # "name_key": row[1].lower(),
            "id": geneRecord['primaryId'],
            # "href": FlyBase.gene_href(row[0]),
            # "category": "gene",
            #"external_ids": []
        }


for gene in genes:
    print gene

for key, value in genes.iteritems() :
    print key, value

#pp.pprint(data)

