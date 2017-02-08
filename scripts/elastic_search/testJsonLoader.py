import json
import argparse
import pprint
import sys

parser = argparse.ArgumentParser(description='Test loader for JSON basic gene info file.')

parser.add_argument('-d', '--data', help='JSON data file', required=True)
args = parser.parse_args()

data_file_name = args.data
with open(data_file_name) as data_file:
    data_content = json.load(data_file)
#    print data_content['data'][0]['primaryId']
    for geneRecord in data_content['data']:
        print geneRecord['primaryId']
        print geneRecord['symbol']
data_file.closed




#pp.pprint(data)

