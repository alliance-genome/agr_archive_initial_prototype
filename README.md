[![Build Status](https://travis-ci.org/alliance-genome/agr_prototype.svg?branch=master)](https://travis-ci.org/alliance-genome/agr_prototype)

# Alliance of Genome Resources Prototype
An initial prototype for the web portal of the Alliance of Genome
Resources.

## Prerequisites

Ensure you've installed [pip][1] and [virtualenv][2] and [nodejs][3].

Create a virtualenv for isolating the python dependencies:

```bash
mkdir -p ~/.virtulanevs/agr_prototype
# The prototype currently requires Python2
virtualenv -p python2 ~/.virtulanevs/agr_prototype
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

