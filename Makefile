BOOTSTRAP = bootstrap.py
BUILDOUT_DEPLOY = buildout_deploy.cfg

build:
	npm install
	npm run build

run:
	FLASK_APP=server.py flask run

tests:
	npm test
