import time

from elasticsearch import Elasticsearch
from mapping import *

es = Elasticsearch("127.0.0.1:9200", timeout=3, retry_on_timeout=False)

myindex = "searchable_items_blue"

new_index = myindex + "_" + str(int(time.time()))

current = es.indices.get(myindex, ignore=[400, 404])
if "status" in current and current["status"] == 404:
	current = None
	current_name = None
else:
	current_name, value = current.popitem()

if current_name != None:
	map = es.indices.get(myindex + "*")
	for i in map:
		if i == current_name:
			print "Current Index: " + i
			continue
		else:
			print "Deleting Old Index: " + i
			es.indices.delete(index=i, ignore=[400, 404])

print "Creating: " + new_index
es.indices.create(index=new_index, body=mapping_schema, ignore=400)

print "Running Index into: " + new_index

if current_name != None:
	print "Remove Alias: " + myindex + " from: " + current_name
	es.indices.delete_alias(index=current_name, name=myindex, ignore=[400, 404])

if current_name != myindex:
	print "Add Alias: " + myindex + " to: " + new_index
	es.indices.put_alias(index=new_index, name=myindex, ignore=[400, 404])
	if current_name != None:
		print "Deleting current: " + current_name
		es.indices.delete(index=current_name, ignore=[400, 404])
else:
	print "Deleting current: " + current_name
	es.indices.delete(index=current_name, ignore=[400, 404])
	print "Add Alias: " + myindex + " to: " + new_index
	es.indices.put_alias(index=new_index, name=myindex, ignore=[400, 404])
