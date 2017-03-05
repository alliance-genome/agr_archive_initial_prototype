# get the Elasticsearch URI from an environment variable, if one is set
ES_HOST := $(or $(ES_HOST),$(ES_HOST),'127.0.0.1:9200')
ES_INDEX := $(or $(ES_INDEX),$(ES_INDEX),'searchable_items_blue')
API_PASSWORD := $(or $(API_PASSWORD),$(API_PASSWORD),'api_password')
PRODUCTION:= $(or $(PRODUCTION),$(PRODUCTION),)

OPTIONS = PRODUCTION=$(PRODUCTION) API_PASSWORD=$(API_PASSWORD) ES_HOST=$(ES_HOST) ES_AWS=$(ES_AWS) ES_INDEX=$(ES_INDEX)

install:
	pip install -r requirements.txt

fetch_and_save:
	cd src && $(OPTIONS) python fetch_and_save.py

load_and_index:
	cd src && $(OPTIONS) python load_and_index.py

index:
	cd sec && $(OPTIONS) python fetch_save_index.py

test:
	$(OPTIONS) nosetests -s
