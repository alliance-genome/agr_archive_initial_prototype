from elasticsearch import Elasticsearch
from mapping_schema import mapping_schema

import os
import time

class ESMapping:

    def __init__(self, es_host, es_index, aws):
        if aws == "true":
            self.es = Elasticsearch(es_host, timeout=30, retry_on_timeout=False, use_ssl=True, verify_certs=True)
        else:
            self.es = Elasticsearch(es_host, timeout=30, retry_on_timeout=False)
        self.es_index = es_index

    def get_current_index(self):
        current = self.es.indices.get(self.es_index, ignore=[400, 404])
        if "status" in current and current["status"] == 404:
            current = None
            current_name = None
        else:
            current_name, value = current.popitem()

        if current_name != None:
            map = self.es.indices.get(self.es_index + "*")
            for i in map:
                if i != current_name:
                    self.delete_index(i)
        return current_name

    def start_index(self):
        self.new_index_name = self.es_index + "_" + str(int(time.time()))
        self.current_name = self.get_current_index()
        print "Current Index: " + str(self.current_name)

        self.create_index(self.new_index_name)

    def finish_index(self):
        if self.current_name != None:
            self.remove_alias(self.es_index, self.current_name)

        if self.current_name != self.es_index:
            self.create_alias(self.es_index, self.new_index_name)
            if self.current_name != None:
                self.delete_index(self.current_name)
        else:
            # This only happens if there is a index existing
            # with the same name missing the time stamp
            # this else can be removed after the initial migration
            self.delete_index(self.current_name)
            self.create_alias(self.es_index, self.new_index_name)

    def create_alias(self, alias, index):
        print "Add Alias: " + alias + " to: " + index
        self.es.indices.put_alias(index=index, name=alias)

    def remove_alias(self, alias, index):
        print "Remove Alias: " + alias + " from: " + index
        self.es.indices.delete_alias(index=index, name=alias, ignore=[400, 404])

    def create_index(self, index):
        print "Creating Index: " + index
        self.es.indices.create(index=index, body=mapping_schema, ignore=400)

    def delete_index(self, index):
        print "Deleting Index: " + index
        self.es.indices.delete(index=index, ignore=[400, 404])

    def index_data(self, data, data_type):
        s = time.time()
        print "Send " + data_type + " into Index: " + self.new_index_name
        bulk_data = []

        for id in data:
            bulk_data.append({
                'index': {
                    '_index': self.new_index_name, 
                    '_type': "searchable_item",
                    '_id': id
                }
            })
            bulk_data.append(data[id])

            if len(bulk_data) == 5000:
                self.es.bulk(index=self.new_index_name, body=bulk_data, refresh=True)
                bulk_data = []

        if len(bulk_data) > 0:
            self.es.bulk(index=self.new_index_name, body=bulk_data, refresh=True)
        print "Indexing took: " + str(time.time() - s) + " seconds"
