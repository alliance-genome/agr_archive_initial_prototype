import time

from elasticsearch import Elasticsearch
from mapping import *

es = Elasticsearch("127.0.0.1:9200", timeout=3, retry_on_timeout=False)

myindex = "searchable_items_blue"
es.indices.delete(index="searchable_items_blue_1488555479", ignore=[400, 404])
es.indices.create(index=myindex, body=mapping_schema, ignore=400)
