[![Build Status](https://travis-ci.org/alliance-genome/agr_prototype.svg?branch=master)](https://travis-ci.org/alliance-genome/agr_prototype)

# Alliance of Genome Resources Prototype
An initial prototype for the web portal of the Alliance of Genome Resources

## Getting started
```bash
$ make build
$ make run
```

To run tests

```bash
$ make tests
```

## Development Environment Pro Tips
Assets are compiled using [webpack](https://webpack.github.io/).  To enable [hot module replacement](https://webpack.github.io/docs/hot-module-replacement.html) in your development environment, run `npm start` while the dev server is running and refresh the page.  Subsequent JavaScript changes will go to your browser as a "hot update" without refreshing.

You can run JavaScript unit tests automatically on each file change by running `npm run test:watch`.

JavaScript coding style is enforced with [ESLint](http://eslint.org/).  The rules are configured in the .eslintrc file.
