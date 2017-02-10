# get the Elasticsearch URI from an environment variable, if one is set
ES_URI := $(or $(ES_URI),$(ES_URI),http://127.0.0.1:9200/)
ES_INDEX := $(or $(ES_INDEX),$(ES_INDEX),'searchable_items_blue')
# if possible have a virtualenv setup first

build:
	npm install
	npm run build
	pip install -r requirements.txt
	cd ~/.virtualenvs/agr_prototype/bin; \
	git clone https://github.com/elelsee/aws-es-connection.git; \
	cd aws-es-connection; \
	python setup.py install

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

index:
	echo $(ES_URI)
	echo $(ES_AWS)
	echo $(ES_INDEX)
	cd scripts/elastic_search && ES_URI=$(ES_URI) ES_AWS=$(ES_AWS) ES_INDEX=$(ES_INDEX) python index.py

test-py:
	nosetests -s
