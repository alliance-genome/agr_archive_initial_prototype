# get the Elasticsearch URI from an environment variable, if one is set
ES_URI := $(or $(ES_URI),$(ES_URI),http://127.0.0.1:9200/)
# if possible have a virtualenv setup first
build:
	npm install
	npm run build
	pip install -r requirements.txt

run:
	ES_URI=$(ES_URI) python src/server.py

run-prod:
	PRODUCTION=true ES_URI=$(ES_URI) gunicorn src.server:app -k gevent --pid gunicorn.pid --daemon

restart:
	kill -s HUP $(cat gunicorn.pid)

stop:
	kill -s TERM $(cat gunicorn.pid)

tests: test-py
	npm test

fetch:
	cd scripts/elastic_search && ES_URI=$(ES_URI) python fetch_data.py

index-files:
	cd scripts/elastic_search && ES_URI=$(ES_URI) python index_data.py

index:
	echo $(ES_URI)
	cd scripts/elastic_search && ES_URI=$(ES_URI) python index.py

test-py:
	nosetests -s
