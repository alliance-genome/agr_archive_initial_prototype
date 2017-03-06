[![Build Status](https://travis-ci.org/alliance-genome/agr.svg?branch=master)](https://travis-ci.org/alliance-genome/agr)

# Alliance of Genome Resources API
A web server of the Alliance of Genome Resources API.

## Prerequisites

Ensure you've installed [pip][1] and [virtualenv][2].

```bash
  Starting with Python 2.7.9, pip is included by default with the Python binary installers. 
  
  make sure the executables node, pip, and virtualenv are accessible from /usr/local/bin  (MAC, Linux)
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

## Getting started


### Setting up a local agr API instance - or on a dev machine

* Local ES hosted INDEX see [elasticsearch setup][4] for more info
* login to your git account - or create one and login
* Go to [alliance-genome/agr_api][3] repository
* Clone your agr copy and checkout the development branch

```bash
   > git clone https://github.com/alliance-genome/agr_api.git
   > cd agr_api
   agr_api> git status  #should show current branch being development if not git checkout development
   agr_api> source ~/.virtualenvs/agr/bin/activate
   agr_api> make      #( to Setup dev working platform )
   agr_api> make run  #( to start your local agr API instance )
```

Now you should be able to use the API, an example URL would be: [http://localhost.jax.org:5000/api/gene/MGI:97490][5] 

* Note* If this link does not work, you might need to run the indexer or you don't have [elasticsearch][4] running, or that Gene no longer exists See [running the indexer][6] for more info.
* If you want to run this in a docker container vs running locally, see the [running docker][7] for more info.
* If you are looking to run the UI web code see the [running the ui][8] for more info.

### Point to remote ES instance

If you don't want to run the ES index locally you can point to the development one. Stop the running server and set these enviroment variables, first.

```bash
	agr_api> export PRODUCTION=true
	agr_api> export ES_AWS=true
	agr_api> export ES_HOST="search-es1-oyqxarxm2djn35dfodzniituhe.us-west-2.es.amazonaws.com"
	agr_api> export ES_INDEX=es1
	agr_api> export API_PASSWORD="api_password"
```

### Point to local ES instance (defaults)

These are the default settings that don't need to be set unless you want to override them.

```bash
	agr_api> export ES_HOST="127.0.0.1:9200"
	agr_api> export ES_INDEX=searchable_items_blue
	agr_api> export API_PASSWORD="api_password"
```

### To run tests

```bash
	agr_api> source ~/.virtualenvs/agr/bin/activate
	agr_api> make tests
```

[1]: https://pip.pypa.io/en/stable/installing/
[2]: https://virtualenv.pypa.io/en/stable/installation/
[3]: https://github.com/alliance-genome/agr_api
[4]: ES_SETUP.md
[5]: http://localhost.jax.org:5000/api/gene/MGI:97490
[6]: https://github.com/alliance-genome/agr_indexer
[7]: DOCKER.md
[8]: https://github.com/alliance-genome/agr_ui
