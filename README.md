[![Continuous Integration Status](https://travis-ci.org/acdaniells/cement.svg?branch=master)](https://travis-ci.org/acdaniells/cement)

# Cement Framework

Cement is an advanced Application Framework for Python, with a primary focus on
Command Line Interfaces (CLI). Its goal is to introduce a standard, and
feature-full platform for both simple and complex command line applications as
well as support rapid development needs without sacrificing quality. Cement is
flexible, and it's use cases span from the simplicity of a micro-framework to
the complexity of a mega-framework. Whether it's a single file script, or a
multi-tier application, Cement is the foundation you've been looking for.

The first commit to Git was on Dec 4, 2009. Since then, the framework has seen
several iterations in design, and has continued to grow and improve since it's
inception. Cement is the most stable, and complete framework for command line
and backend application development.

## Core Features

Cement core features include (but are not limited to):

- Core pieces of the framework are customizable via handlers/interfaces
- Handler system connects implementation classes with Interfaces
- Extension handler interface to easily extend framework functionality
- Config handler supports parsing multiple config files into one config
- Argument handler parses command line arguments and merges with config
- Log handler supports console and file logging
- Plugin handler provides an interface to easily extend your application
- Output handler interface renders return dictionaries to console
- Cache handler interface adds caching support for improved performance
- Controller handler supports sub-commands, and nested controllers
- Hook support adds a bit of magic to apps and also ties into framework
- Zero external dependencies* (not including optional extensions)
- 100% test coverage (`pytest`)
- 100% PEP8 compliant (`flake8`)
- Extensive API Reference (`sphinx`)
- Tested on Python 3.6+
- Does not support Python 2.x

*Some optional extensions that are shipped with the mainline Cement sources do
*require external dependencies. It is the responsibility of the application
*developer to include these dependencies along with their application, as Cement
*explicitly does not include them.*

## More Information

Links to the original package:

- [Official Website / Developer Documentation](http://builtoncement.com/)
- [PyPi Packages](http://pypi.python.org/pypi/cement/)
- [GitHub Source Code / Issue Tracking](http://github.com/datafolklabs/cement/)

## License

The Cement CLI Application Framework is Open Source and is distributed under the
BSD License (three clause). Please see the LICENSE file included with this
software.

## Development

See `Makefile` for all common development actions.

### Virtual Environment Manager

A venv helper is available:

```shell
$ make develop

$ source env/bin/activate

(env) $

deactivate
```

### Running Tests and Compliance

Cement has a strict policy that all code and tests meet PEP8 guidelines,
therefore `flake8` is called before any unit tests run. All code submissions
require 100% test coverage and PEP8 compliance:

Execute the following to run all unit tests:

```shell
$ make test
```

Execute the following to run all compliance tests:

```shell
$ make comply
```

Execute the following to sort imports and format the source code using `black`:

```shell
$ make format
```

Note that a set of Pre-commit hooks are also defined within the project.

### Documentation

Execute the following to build the Cement documentation:

```shell
$ make docs
```

### Release

Once a round of development is completed you will need to generate the
distribution archives for release. Firstly, update the version in the following
locations and create a tag in the git repository.

* cement/core/backend.py
* cement/tests/core/test_backend.py
* cement/tests/utils/test_version.py

To generate the distribution archives Execute the following:

```shell
make dist
```

This should generate two files in the `dist` directory:

```
dist/
  cement-3.1.0-py3-none-any.whl
  cement-3.1.0.tar.gz
```

The `tar.gz` file is a source archive whereas the `whl` file is a built
distribution.
