# get the Elasticsearch URI from an environment variable, if one is set
ES_URI := $(or $(ES_URI),$(ES_URI),http://127.0.0.1:9200/)
ES_INDEX := $(or $(ES_INDEX),$(ES_INDEX),'searchable_items_blue')

# if possible have a virtualenv setup first

build:
	npm install
	npm run build
	pip install -r requirements.txt

run:
	ES_URI=$(ES_URI) ES_AWS=$(ES_AWS) ES_INDEX=$(ES_INDEX) python src/server.py

run-prod:
	PRODUCTION=true ES_URI=$(ES_URI) gunicorn src.server:app -k gevent --pid gunicorn.pid --daemon

restart:
	kill -s HUP $(cat gunicorn.pid)

stop:
	kill -s TERM $(cat gunicorn.pid)

tests: test-py
	ES_INDEX=$(ES_INDEX) npm test

fetch_and_save:
	cd scripts/elastic_search && ES_INDEX=$(ES_INDEX) ES_URI=$(ES_URI) python fetch_and_save.py

load_and_index:
	cd scripts/elastic_search && ES_INDEX=$(ES_INDEX) ES_URI=$(ES_URI) python load_and_index.py

index:
	cd scripts/elastic_search && ES_INDEX=$(ES_INDEX) ES_URI=$(ES_URI) python fetch_save_index.py

test-py:
	nosetests -s
