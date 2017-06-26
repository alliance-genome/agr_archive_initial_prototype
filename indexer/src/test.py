from elasticsearch import Elasticsearch

es = Elasticsearch("https://search-es1-oyqxarxm2djn35dfodzniituhe.us-west-2.es.amazonaws.com", timeout=30, retry_on_timeout=False, use_ssl=True, verify_certs=True)



print es.indices.delete(index="es2_1491847190")
