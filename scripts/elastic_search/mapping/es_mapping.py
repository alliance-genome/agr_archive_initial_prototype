from elasticsearch import Elasticsearch
from mapping_schema import mapping_schema

import os
import time
import requests

class ESMapping:

    def __init__(self, es_uri, es_index, aws):
        if aws == "true":
            self.es = Elasticsearch(es_uri, timeout=5, retry_on_timeout=False, use_ssl=True, verify_certs=True)
        else:
            self.es = Elasticsearch(es_uri, timeout=5, retry_on_timeout=False)
        self.es_uri = es_uri
        self.es_index = es_index

    def start_index(self):
        self.es_index_tmp = self.es_index + "_tmp"
        #self.delete_index(self.es_index_tmp)
        self.create_index(self.es_index_tmp)

    def finish_index(self):
        self.delete_index(self.es_index)
        self.create_index(self.es_index)
        self.copy_index(self.es_index_tmp, self.es_index)
        self.delete_index(self.es_index_tmp)

    def create_index(self, index):
        from mapping_schema import mapping_schema
        s = time.time()

        print "Creating Index: " + self.es_uri + index + "/"
        response = requests.put(self.es_uri + index + "/", json=mapping_schema)
        if response.status_code != 200:
            print "ERROR: " + response.json()['error']['reason']
        else:
            print "SUCCESS: " + str(time.time() - s) + " seconds"

    def delete_index(self, index):
        s = time.time()
        print "Deleting Index: " + self.es_uri + index + "/"
        response = requests.delete(self.es_uri + index + "/")
        if response.status_code != 200:
            print "WARNING: " + response.json()['error']['reason']
        else:
            print "SUCCESS: " + str(time.time() - s) + " seconds"

    def copy_index(self, index_src, index_dst):
        s = time.time()
        print "Copying Documents from: " + index_src + " to " + index_dst

        response = requests.post(self.es_uri + "_reindex", data='{ "source": { "index": "' + self.es_index_tmp + '" }, "dest": { "index": "' + self.es_index + '" } }')
        if response.status_code != 200:
            print "ERROR: " + response.json()['error']['reason']
        else:
            print "SUCCESS: " + str(time.time() - s) + " seconds"

    def index_data(self, data):
        s = time.time()
        print "Send data into Index: " + self.es_index_tmp
        bulk_data = []

        for id in data:
            bulk_data.append({
                'index': {
                    '_index': self.es_index_tmp, 
                    '_type': "searchable_item",
                    '_id': id
                }
            })
            bulk_data.append(data[id])

            if len(bulk_data) == 5000:
                self.es.bulk(index=self.es_index_tmp, body=bulk_data, refresh=True)
                bulk_data = []

        if len(bulk_data) > 0:
            self.es.bulk(index=self.es_index_tmp, body=bulk_data, refresh=True)
        print "Indexing took: " + str(time.time() - s) + " seconds"
