PY_VERSION ?= $(shell python -c 'import sys;print(sys.version_info.major)')
VENV_HOME := ${HOME}/.virtualenvs
VENV_NAME := agr_prototype-py${PY_VERSION}
VENV_PATH := ${VENV_HOME}/${VENV_NAME}
VENV_BIN := ${VENV_PATH}/bin
VENV_PIP := ${VENV_BIN}/pip
VENV_PYTHON := ${VENV_BIN}/python
VENV_NOSETESTS := ${VENV_BIN}/nosetests

define print-help
        $(if $(need-help),$(warning $1 -- $2))
endef

need-help := $(filter help,$(MAKECMDGOALS))

help: ; @echo $(if $(need-help),,\
	Type \'$(MAKE)$(dash-f) help\' to get help)

.PHONY: run-prod
run-prod: $(call print-help,run-prod,"Run the production server.")
	PRODUCTION=true ES_URI=${ES_URI}  gunicorn src.server:app \
                        -k gevent \
                        --pid gunicorn.pid \
                        --daemon
.PHONY: restart-prod
restart-prod: $(call print-help,restart-prod,\
"Restart the production server")
	kill -s HUP $(cat gunicorn.pid)

.PHONY: stop-prod
stop-prod: $(call print-help,stop-prod,"Stop the production server.")
	kill -s TERM $(cat gunicorn.pid)

.PHONY: py-virtualenv
py-virtualenv: $(call print-help,py-virtualenv,"Creates a Python virtualenv")
	@mkdir -p ${VENV_PATH}
	@virtualenv -p python${PY_VERSION} ${VENV_PATH}

.PHONY: build
build: $(call print-help,build,"Builds all dependencies for the project.") \
	py-virtualenv
	@npm install
	@npm run build
	@${VENV_PIP} install -r requirements.txt

.PHONY: run
run: $(call print-help,run,"Runs the application server.")
	ES_URI=${ES_URI} ${VENV_PYTHON} src/server.py

.PHONY: tests
tests: $(call print-help,tests,"Runs all tests for the project.") \
	test-py
	@npm test

.PHONY: index
index: $(call print-help,index,"Indexes data into elasticsearch.")
	@cd scripts/elastic_search
	ES_URI=${ES_URI} python index.py

.PHONY: test-py
test-py: $(call print-help,test-py,"Runs the Python test suite.")
	@${VENV_NOSETESTS} -s
