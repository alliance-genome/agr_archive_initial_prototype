ES_URI=http://35.160.110.142:9200/

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

index:
	cd scripts/elastic_search && ES_URI=$(ES_URI) python index.py

test-py:
	nosetests -s
