[![Build Status](https://travis-ci.org/alliance-genome/agr_prototype.svg?branch=master)](https://travis-ci.org/alliance-genome/agr_prototype)

# Alliance of Genome Resources Prototype
An initial prototype for the web portal of the Alliance of Genome
Resources.

## Prerequisites

Ensure you've installed [pip][1] and [virtualenv][2] and [nodejs][3].

Create a virtualenv for isolating the python dependencies:

```bash
mkdir -p ~/.virtualenvs/agr_prototype
# The prototype currently requires Python2
virtualenv -p python2 ~/.virtualenvs/agr_prototype
```

## Getting started
```bash
source ~/.virtualenvs/agr_prototype/bin/activate
make build
make run
```

To run tests

```bash
source ~/.virtualenvs/agr_prototype/bin/activate
make tests
```

## Docker

You can also use Docker to install and develop with the AGR web portal.  Advantages of
this include:

* No need to install elasticsearch
* Simplifies running multiple instances on a single host.

### Getting started with Docker

1. Install [Docker and Docker Compose](https:///www.docker.com/products/overview)

Be sure to install both, some OS packages bundle them together and some do not.

2. Clone the git repo.

3. Build and start docker containers

`docker-compose up` or `docker-compose up -d` 

The `-d` option will put the containers in the background.

Once up, you should be able to access the server at http://localhost:5000/

Any changes to the React application should be rebuilt by the webpack container
and available via the above URL.  Changes to the python code currently require that
the container be rebuilt.

### Elasticsearch indexing

This command will call the `index` target in the Makefile.  This should be
used after your first start or if you want to re-index.

`docker-compose exec agr make index`

### Description

This Docker setup uses 3 containers to manage the AGR portal.

1. Elasticsearch - db
2. Flask server  - agr
3. Webpack/node  - webpack

The Flask and Webpack containers expose external ports on 5000 and 2992 respectively.
The elasticsearch db container is exposed only to the Flask server container by default.

The webpack container uses the [hot module replacement][5] mode by default.

## Development Environment Pro Tips
Assets are compiled using [webpack][4]. 
To enable [hot module replacement][5] in your development environment,
run `npm start` while the dev server is running and refresh the page.
Subsequent JavaScript changes will go to your browser as a "hot
update" without refreshing.

You can run JavaScript unit tests automatically on each file change by
running `npm run test:watch`.

JavaScript coding style is enforced with [ESLint][6].
The rules are configured in the .eslintrc file.

[1]: https://pip.pypa.io/en/stable/installing/
[2]: https://virtualenv.pypa.io/en/stable/installation/
[3]: https://docs.npmjs.com/getting-started/installing-node
[4]: https://webpack.github.io/
[5]: https://webpack.github.io/docs/hot-module-replacement.html
[6]: http://eslint.org/

