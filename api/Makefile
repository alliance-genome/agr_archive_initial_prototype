# get the Elasticsearch URI from an environment variable, if one is set
ES_HOST := $(or $(ES_HOST),$(ES_HOST),'127.0.0.1:9200')
ES_INDEX := $(or $(ES_INDEX),$(ES_INDEX),'searchable_items_blue')
API_PASSWORD := $(or $(API_PASSWORD),$(API_PASSWORD),'api_password')
BEHAVE_TEST_URL := $(or $(BEHAVE_TEST_URL),$(BEHAVE_TEST_URL),'http://localhost:2992')
PRODUCTION:= $(or $(PRODUCTION),$(PRODUCTION),)

OPTIONS = PRODUCTION=$(PRODUCTION) API_PASSWORD=$(API_PASSWORD) ES_HOST=$(ES_HOST) ES_AWS=$(ES_AWS) ES_INDEX=$(ES_INDEX)

install:
	pip install -r requirements.txt

run:
	$(OPTIONS) python src/server.py

run-prod:
	cd src && $(OPTIONS) gunicorn server:app -k gevent --pid gunicorn.pid --daemon

restart:
	kill -s HUP $(cat gunicorn.pid)

stop:
	kill -s TERM $(cat gunicorn.pid)

fetch_and_save:
	cd scripts/elastic_search && $(OPTIONS) python fetch_and_save.py

load_and_index:
	cd scripts/elastic_search && $(OPTIONS) python load_and_index.py

test_index:
	cd scripts/elastic_search && $(OPTIONS) python fetch_save_test_index.py

index:
	cd scripts/elastic_search && $(OPTIONS) python fetch_save_index.py

tests: test-py test-end-to-end

test-py:
	$(OPTIONS) nosetests -s test

test-end-to-end:
	BEHAVE_TEST_URL=$(BEHAVE_TEST_URL) behave test/functional_tests
