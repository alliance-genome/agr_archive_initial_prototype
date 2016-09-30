ES_URI=http://52.43.223.105:9200/
BOOTSTRAP = bootstrap.py
BUILDOUT_DEPLOY = buildout_deploy.cfg

# if possible have a virtualenv setup first
build:
	npm install
	npm run build
	pip install -r requirements.txt

run:
	FLASK_APP=src/server.py flask run

tests:
	npm test

index:
	cd scripts/elastic_search && ES_URI=$(ES_URI) python index.py
