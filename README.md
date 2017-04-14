# Alliance of Genome Resources (AGR)
[![Build status](https://travis-ci.org/alliance-genome/agr.svg?branch=master)](https://travis-ci.org/alliance-genome/agr)
[![Overall test coverage](https://coveralls.io/repos/github/alliance-genome/agr/badge.svg?branch=master)](https://coveralls.io/github/alliance-genome/agr)
[![Code Climate](https://codeclimate.com/github/alliance-genome/agr.svg)](https://codeclimate.com/github/alliance-genome/agr)
[![Core Infrastructure Initiative Best Practices](https://bestpractices.coreinfrastructure.org/projects/864/badge)](https://bestpractices.coreinfrastructure.org/projects/864)

This software is written to support the goals of [Alliance of Genome Resources](http://www.alliancegenome.org/)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Contents

- [Prerequisites](#prerequisites)
- [Installing](#installing)
- [Configuration](#configuration)
  * [Webapp](#webapp)
  * [API](#api)
  * [Indexer](#indexer)
  * [ElasticSearch](#elasticsearch)
- [Running the Enviroment](#running-the-enviroment)
  * [Webapp](#webapp-1)
  * [API](#api-1)
  * [Indexer](#indexer-1)
  * [ElasticSearch](#elasticsearch-1)
- [API Usage](#api-usage)
- [Running the tests](#running-the-tests)

## Prerequisites

- NodeJS
- Python 2.7
- Python Package Index (pip)
- Virtualenv
- Elasticsearch

```bash
  Starting with Python 2.7.9, pip is included by default with the Python binary installers. 
  
  make sure the executables npm, node, pip, and virtualenv are accessible from /usr/local/bin  (MAC, Linux)
  if not create symbolic links as needed
  
  Make sure /usr/local/bin is in your PATH (MAC, Linux)
```
Create a virtualenv for isolating the python dependencies:

```bash
	> mkdir -p ~/.virtualenvs/agr
	> # The prototype currently requires Python2
	> # Assuming virtualenv and python2 are in your PATH
	> virtualenv -p python2 ~/.virtualenvs/agr
```
* Webapp requires (NodeJS)
* API requires (python, pip, virtualenv, Elasticsearch)
* Indexer requires (python, pip, virtualenv, Elasticsearch)

Local ES hosted INDEX see [elasticsearch setup][4] for more info

## Installing

To run a full install of all sub directories run the following:

```bash
   (agr) > git clone https://github.com/alliance-genome/agr.git
   (agr) > cd agr
   (agr) agr> source ~/.virtualenvs/agr/bin/activate
   (agr) agr> make -C webapp install
   (agr) agr> make -C webapp build
   (agr) agr> make -C api install
   (agr) agr> make -C indexer install
```

## Configuration

### Webapp

- API_URL A url pointing to the server that is hosting the /api endpoint for the frontend
- DEV\_SERVER\_UI\_PORT Used to specify the local port that the WEBPACK server will be listening on

These params default to localhost and 2992, but if you want to override them then run the following:

```bash
   (agr) agr> cd webapp
   (agr) agr/webapp> export API_URL=http://dev.alliancegenome.org
   (agr) agr/webapp> export DEV_SERVER_UI_PORT=12345
```

After running the WEBPACK server, the server will be running on http://localhost:12345 making calls to the API running at dev.alliancegenome.org.

### API

- PRODUCTION Used to control the start up of the flask server. If set to false then debugging will be turned on and the server will crash upon first encountered error. If set to true then the server runs the WSGIServer.
- ES\_AWS Used to control wether or not SSL will be used on the connection to ES_HOST.
- ES\_HOST Used to point the flask server to the running Elastic Search instance.
- ES\_INDEX Used to indicate which index the flask server will be using to get its data.
- API\_PASSWORD Not used at the moment, but will be the password controlling access to the writable API's

```bash
	(agr) agr> cd api
	(agr) agr/api> export PRODUCTION=true
	(agr) agr/api> export ES_AWS=true
	(agr) agr/api> export ES_HOST="search-es1-oyqxarxm2djn35dfodzniituhe.us-west-2.es.amazonaws.com"
	(agr) agr/api> export ES_INDEX=es_username
	(agr) agr/api> export API_PASSWORD="api_password"
```

The defaults for these variables are set to:

- PRODUCTION = false
- ES\_AWS = false
- ES\_HOST = "http://localhost:9200"
- ES\_INDEX = searchable_items_blue
- API\_PASSWORD = "api_password"

### Indexer

- ES\_AWS Used to control wether or not SSL will be used on the connection to ES_HOST.
- ES\_HOST Used to point the flask server to the running Elastic Search instance.
- ES\_INDEX Used to indicate which index the flask server will be using to get its data.

```bash
	(agr) agr> cd indexer
   (agr) agr/indexer> export ES_AWS=true
   (agr) agr/indexer> export ES_HOST="search-es1-oyqxarxm2djn35dfodzniituhe.us-west-2.es.amazonaws.com"
   (agr) agr/indexer> export ES_INDEX=es_username
```

The defaults for these params point to the localhost running elasticsearch.

### ElasticSearch

There is no configuration for ElasticSearch please see the [elasticsearch setup][4] for more info

## Running the Enviroment

All the following steps are not nessasary, if one wants to only develop part of the system. The frontend (webapp) can be pointed to a different API server and the webpack dev server will run on its own without the API, Indexer, or ES running.

Simularly if only the API needs to be developed then one can start the API and point the ES_HOST to somewhere that already has data and there is no need to run the webapp, indexer, or elasticsearch instance.

Also simularly if someone is developing the indexer, they can go through the local setup of the elasticsearch and point the indexer to run against the localhost elasticsearch with out having to run the API or webapp.

### Webapp

In a seperate terminal window run the following:

```bash
	(agr) agr> make -C webapp run
npm start

> agr@0.0.5 start /Users/oblod/git/agr/webapp
> webpack-dev-server --history-api-fallback --hot --inline

[HPM] Proxy created: /api  ->  http://localhost:5000
 http://localhost:2992/
webpack result is served from /assets/
content is served from dist
404s will fallback to /index.html
The react/require-extension rule is deprecated. Please use the import/extensions rule from eslint-plugin-import instead.
The react/wrap-multilines rule is deprecated. Please use the react/jsx-wrap-multilines rule instead.
```

Now the server is running on port 2992 and proxying /api requests to localhost:5000 which should be the running flask server.

### API

In a seperate terminal window run the following:

```bash
	(agr) agr> make -C api run
	PRODUCTION= API_PASSWORD='api_password' ES_HOST='127.0.0.1:9200' ES_AWS= ES_INDEX='searchable_items_blue' python src/server.py
	 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
	 * Restarting with stat
	 * Debugger is active!
	 * Debugger pin code: 326-018-460
```

### Indexer

In a seperate terminal window run the following:

```bash

	(agr) agr> make -C indexer index
	cd src && ES_HOST='127.0.0.1:9200' ES_AWS= ES_INDEX='searchable_items_blue' python fetch_save_index.py
	ES_HOST: 127.0.0.1:9200
	ES_INDEX: searchable_items_blue
	ES_AWS: 
	...
	...
	...
	>
```

After the indexer has run, the Elastic search instance will be loaded with data that is now available to the API.

### ElasticSearch

For running a local ElasticSearch instance see the [elasticsearch setup][4] for more info

## API Usage



## Running the tests


[4]: doc/ES_SETUP.md
