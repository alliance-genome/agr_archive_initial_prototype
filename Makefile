ES_URI=http://52.43.223.105:9200/

# if possible have a virtualenv setup first
build:
	npm install
	npm run build
	pip install -r requirements.txt

run:
	ES_URI=$(ES_URI) python src/server.py

tests: test-py
	npm test

index:
	cd scripts/elastic_search && ES_URI=$(ES_URI) python index.py

test-py:
	flake8 test src
	nosetests -s
