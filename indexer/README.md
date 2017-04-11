[![Build Status](https://travis-ci.org/alliance-genome/agr.svg?branch=master)](https://travis-ci.org/alliance-genome/agr)

# Alliance of Genome Resources Indexer
An initial prototype for the web portal of the Alliance of Genome
Resources.

## Prerequisites

Ensure you've installed [pip][1] and [virtualenv][2].

```bash
  Starting with Python 2.7.9, pip is included by default with the Python binary installers. 
  
  make sure the executables pip, and virtualenv are accessible from /usr/local/bin  (MAC, Linux)
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

### Setting up a local agr Indexer - or on a dev machine

* Local ES hosted INDEX see [elasticsearch setup][4] for more info
* login to your git account - or create one and login
* Go to [alliance-genome/agr_indexer][3] repository
* Clone your agr copy and checkout the development branch

```bash
   > git clone https://github.com/alliance-genome/agr_indexer.git
   > cd agr_indexer
   agr_indexer> git status  #should show current branch being development if not git checkout development
   agr_indexer> source ~/.virtualenvs/agr/bin/activate
   agr_indexer> make        #( to Setup dev working platform )
   agr_indexer> make index  #( to start running data into the index )
```
```
Make sure the Elastic search instance is running before running the command "make index" otherwise it will fail

```

[1]: https://pip.pypa.io/en/stable/installing/
[2]: https://virtualenv.pypa.io/en/stable/installation/
[3]: https://github.com/alliance-genome/agr_indexer
[4]: https://github.com/alliance-genome/agr_api/ES_SETUP.md
