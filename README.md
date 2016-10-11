[![Build Status](https://travis-ci.org/alliance-genome/agr_prototype.svg?branch=master)](https://travis-ci.org/alliance-genome/agr_prototype)

# Alliance of Genome Resources Prototype
An initial prototype for the web portal of the Alliance of Genome Resources

## Getting started

### Python setup

### Install Python development libraries/header files
This is required as the project uses some C-compiled components.

On Ubuntu 16.04:

```bash
sudo apt-get install libpython-dev
```

#### Install pip and virtualenv
[pip][1] is the de-facto Python package manager.
[virtualenv][2] isolates the installation of Python packages for this
project from your system environment.

You may want to look into installing [virtualenvwrapper][3] for
convenience.


```bash
$ make build
$ make run
```

#### Create a virtualenv and activate it.

Python 3 example:
```bash
VENV_HOME="${HOME}/.virtualenvs"
mkdir -p "${VENV_HOME}"
virtualenv -p python3 "${VENV_HOME}/agr_prototype"
source "${VENV_HOME}/bin/activate
```

<small>Hint: type `deactivate` to exit the virtualenv and return to your
regular prompt.</small>

To run tests

```bash
$ make tests
```

## Development Environment Pro Tips
Assets are compiled using [webpack](https://webpack.github.io/).  To enable [hot module replacement](https://webpack.github.io/docs/hot-module-replacement.html) in your development environment, run `npm start` while the dev server is running and refresh the page.  Subsequent JavaScript changes will go to your browser as a "hot update" without refreshing.

You can run JavaScript unit tests automatically on each file change by running `npm run test:watch`.

JavaScript coding style is enforced with [ESLint](http://eslint.org/).  The rules are configured in the .eslintrc file.


[1]: https://pip.pypa.io/en/stable/installing/
[2]: https://virtualenv.pypa.io/en/stable/
[3]: https://virtualenvwrapper.readthedocs.io/en/latest/
