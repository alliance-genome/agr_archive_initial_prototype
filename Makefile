BOOTSTRAP = bootstrap.py
BUILDOUT_DEPLOY = buildout_deploy.cfg

build:
	npm install
	npm run build
	pip install -r requirements.txt

run:
	FLASK_APP=src/server.py flask run

tests:
	npm test
