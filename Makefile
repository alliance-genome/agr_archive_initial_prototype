# get the Elasticsearch URI from an environment variable, if one is set
ES_URI := $(or $(ES_URI),$(ES_URI),http://127.0.0.1:9200/)
ES_INDEX := $(or $(ES_INDEX),$(ES_INDEX),'searchable_items_blue')
API_PASSWORD := $(or $(API_PASSWORD),$(API_PASSWORD),'api_password')
PRODUCTION:= $(or $(PRODUCTION),$(PRODUCTION),)

OPTIONS = PRODUCTION=$(PRODUCTION) API_PASSWORD=$(API_PASSWORD) ES_URI=$(ES_URI) ES_AWS=$(ES_AWS) ES_INDEX=$(ES_INDEX) DATABASE_URL=$(DATABASE_URL)

# if possible have a virtualenv setup first

build:
	npm install
	npm run build
	pip install -r requirements.txt

run:
	$(OPTIONS) python src/server.py

run-prod:
	cd src && $(OPTIONS) gunicorn server:app -k gevent --pid gunicorn.pid --daemon

restart:
	kill -s HUP $(cat gunicorn.pid)

stop:
	kill -s TERM $(cat gunicorn.pid)

tests: test-py test-js

fetch_and_save:
	cd scripts/elastic_search && $(OPTIONS) python fetch_and_save.py

load_and_index:
	cd scripts/elastic_search && $(OPTIONS) python load_and_index.py

index:
	cd scripts/elastic_search && $(OPTIONS) python fetch_save_index.py

test-py:
	$(OPTIONS) nosetests -s

test-js:
	$(OPTIONS) npm test
