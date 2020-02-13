Cement Framework
================

.. image:: https://img.shields.io/badge/codecov-70%25-success?logo=codecov

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/ambv/black

.. image:: https://img.shields.io/badge/license-BSD-blueviolet
   :target: https://tfs.gsk.com/tfs/PlatformProduct/qcanalysis/_git/cement?path=%2FLICENSE&version=GBmaster

.. image:: https://img.shields.io/badge/release-v3.1.0-blueviolet

.. image:: https://img.shields.io/badge/python-3.6-blueviolet

.. image:: https://img.shields.io/badge/platform-linux-lightgrey

.. note::

   This internal GSK project is derived from the Data Folk Labs Cement project
   available on `GitHub <https://github.com/datafolklabs/cement>`_.

What is Cement?
---------------

Cement is an advanced application framework for Python, with a primary focus on
Command Line Interfaces (CLI). Its goal is to introduce a standard, and
feature-full platform for both simple and complex command line applications as
well as support rapid development needs without sacrificing quality. Cement is
flexible, and its use cases span from the simplicity of a micro-framework to the
complexity of a mega-framework. Whether its a single file script, or a
multi-tier application, Cement is the foundation you've been looking for.

The first commit to Git was on Dec 4, 2009. Since then, the framework has seen
several iterations in design, and has continued to grow and improve since its
inception. Cement is the most stable, and complete framework for command line
and backend application development.

Core Features
-------------

Cement core features include (but are not limited to):

* Core pieces of the framework are customizable via handlers/interfaces
* Extension handler to easily extend framework functionality
* Config handler merges defaults, multiple files, and environment variables into one config
* Argument handler parses command line arguments and options
* Log handler supports logging to console and file
* Plugin handler provides the ability to easily extend your application
* Output handler renders data to the end-user (often via template handler backends)
* Template handler renders content and file templates
* Cache handler adds caching support for improved performance or key/value storage
* Controller handler supports sub-commands, and nested/embedded controllers
* Hook support adds a bit of magic to apps and also ties into framework
* Zero external dependencies\* (not including optional extensions)
* 100% test coverage using `pytest` and `coverage`
* 100% PEP8 and style compliant using `flake8`
* Extensive Developer Guide and API Reference Documentation
* Tested on Python 3.5+
* Does not support Python 2.x

*Some optional extensions that are shipped with the mainline Cement sources do
require external dependencies. It is the responsibility of the application
developer to include these dependencies along with their application, as Cement
explicitly does not include them.*

License
-------

The Cement Framework is Open Source and is distributed under the :ref:`BSD License
(three clause) <https://opensource.org/licenses/BSD-3-Clause>`. Copyright (c)
2009-2018 Data Folk Labs, LLC. All rights reserved.

.. toctree::
   :maxdepth: 2
   :caption: Developer Guide

   docs/changelog

   docs/getting-started/README

   docs/core-foundation/README

   docs/extensions/README

   docs/utilities/README

   docs/additional-topics/README

   docs/terminology

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/core/index
   api/ext/index
   api/utils/index
