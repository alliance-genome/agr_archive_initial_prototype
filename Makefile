
build: build-frontend build-backend

build-frontend:
	npm install
	npm run build

build-backend:
	pip install -r requirements.txt

run:
	python src/server.py

db:
	cd src && python manager.py db

db-init:
	cd src && python manager.py db init

db-migrate:
	cd src && python manager.py db migrate

db-upgrade:
	cd src && python manager.py db upgrade

run-prod:
	cd src && gunicorn server:app -k gevent --pid gunicorn.pid --daemon

restart:
	kill -s HUP $(cat gunicorn.pid)

stop:
	kill -s TERM $(cat gunicorn.pid)

tests: test-py test-js

fetch_and_save:
	cd scripts/elastic_search && python fetch_and_save.py

load_and_index:
	cd scripts/elastic_search && python load_and_index.py

index:
	cd scripts/elastic_search && python fetch_save_index.py

test-py:
	nosetests -s

test-js:
	npm test
