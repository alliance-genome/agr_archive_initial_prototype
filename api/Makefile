# get the Elasticsearch URI from an environment variable, if one is set
ES_HOST := $(or $(ES_HOST),$(ES_HOST),'127.0.0.1:9200')
ES_INDEX := $(or $(ES_INDEX),$(ES_INDEX),'searchable_items_blue')
API_PASSWORD := $(or $(API_PASSWORD),$(API_PASSWORD),'api_password')
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

test:
	$(OPTIONS) nosetests -s
