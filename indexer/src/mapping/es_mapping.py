from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk
from mapping_schema import mapping_schema

import os
import time

class ESMapping:

    def __init__(self, es_host, es_index, aws, chunk_size):
        self.chunk_size = chunk_size
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
        print "Finished loading, refreshing index."
        self.es.indices.refresh(index=self.new_index_name)

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

    def index_data(self, data, data_type, op_type):
        s = time.time()
        bulk_data = []
        id_to_use = None

        print "Indexing %s into Index: %s." % (data_type, self.new_index_name)

        for entry in data:
            if data_type == "Gene Data":
                id_to_use = entry['primaryId']
                doc = entry
            elif data_type == "GO Data" or data_type == "DO Data":
                id_to_use = data[entry]['id']
                doc = data[entry]
                
            doc.update(
                {   '_op_type': op_type,
                    '_index': self.new_index_name, 
                    '_type': "searchable_item",
                    '_id': id_to_use,
                })
            bulk_data.append(doc)

        for success, info in streaming_bulk(self.es, actions=bulk_data, refresh=False, request_timeout=60, chunk_size=self.chunk_size):
                if not success:
                    print "A document failed: %s" % (info)

        print "Indexing took: " + str(time.time() - s) + " seconds"