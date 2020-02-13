# Part 1: Creating Your First Project

## Introduction

Throughout this tutorial we will be building a task management application called `todo`. We will begin with a barebones template using the `cement generate` tool, and build up from there to cover as much of the core features of the framework as possible.

Our application will include the following features:

* Ability to create, update, and delete task items
* List and display tasks via [Jinja2](../../extensions/jinja2.md) templates
* Persist data using [TinyDB](http://tinydb.readthedocs.io/en/latest/intro.html)
* Send an email message when tasks are complete

A [video walk-thru](https://builtoncement.com/assets/video/beginner-tutorial.mp4) of the tutorial is also available.

## Generating a New Project Repository

Cement includes a [developer utility](../developer-tools.md) called `cement` that includes tools to make our lives easier. This was introduced in Cement 3, and will continue to grow as feature requests are made for new and improved ways of streamlining the development process.

Create a new project with the following command and parameters:

```text
$ cement generate project ./todo
INFO: Generating cement project in ./todo
App Label [myapp]: todo
App Name [My Application]: My TODO Application
App Class Name [MyApp]: Todo
App Description [MyApp Does Amazing Things!]: A Simple TODO Application
Creator Name [John Doe]: Your Name
Creator Email [john.doe@example.com]: you@yourdomain.com
Project URL [https://github.com/johndoe/myapp/]: https://github.com/yourname/todo/
License [unlicensed]:
```

## Exploring The TODO Project

The following covers the primary components included with your new project. First, take a look at the generated directory:

```text
.
├── CHANGELOG.md
├── Dockerfile
├── LICENSE.md
├── MANIFEST.in
├── Makefile
├── README.md
├── config
│   └── todo.yml.example
├── docs
├── requirements-dev.txt
├── requirements.txt
├── setup.cfg
├── setup.py
├── tests
│   ├── conftest.py
│   └── test_main.py
└── todo
    ├── controllers
    │   └── base.py
    ├── core
    │   ├── exc.py
    │   └── version.py
    ├── ext
    ├── main.py
    ├── plugins
    └── templates
        └── command1.jinja2

9 directories, 24 files
```

This looks like a lot, however there is a lot of placeholders here for best practice or recommended design. Keep in mind, a Cement application can be as simple as a single file script... however we know that our TODO application will be disrupting the industry of task management, therefore we want to start things on the right track.

Let's break this down into more manageable pieces:

**Common Project Files**

```text
├── CHANGELOG.md
├── LICENSE.md
├── README.md
```

These files should look familiar as they are common in most projects. The `README.md` is populated with some starter info to help get more familiar with the layout and navigation of the project. You should read the `README.md` now.

**Common Python Packaging Files**

```text
├── MANIFEST.in
├── requirements-dev.txt
├── requirements.txt
├── setup.cfg
├── setup.py
```

These files should look familiar to anyone who has packaged and distributed a Python project before, and are required for proper installation, setup, and distribution. Note that the `requirements.txt` lists dependencies that are strictly required for deployment \(production\), where the additional `requirements-dev.txt` includes additional dependencies that are only required for development \(running tests, building documentation, etc\).

**Miscellaneous Development Files**

```text
├── Dockerfile
├── Makefile
```

The included `Dockerfile` gives you a working Docker image out-of-the box, while the `Makefile` includes several helpers for common development tasks such as creating a virtualenv, running tests, building docker, etc.

**Default Configuration, Documentation, and Tests**

```text
├── config
│   └── todo.yml.example
├── docs
├── tests
│   ├── conftest.py
│   └── test_main.py
```

A good application has excellent documentation and testing, along with example configuration files of the applications settings \(and their defaults\). As configuration defaults are added \(or modified\) in the application, the `config/todo.yml.example` should be updated to reflect them.

**Our Application Module**

```text
└── todo
    ├── controllers
    │   └── base.py
    ├── core
    │   ├── exc.py
    │   └── version.py
    ├── ext
    ├── main.py
    ├── plugins
    └── templates
        └── command1.jinja2
```

Finally, our code lives in a python module called `todo`, with what should be an obvious breakdown of submodules that clearly separate code into relevant and organized buckets. Take a moment to briefly review all of the files provided in the generated project repository.

Again, note that a Cement project does not need to be organized this way but is a solid starting point to streamline development. If you aren't entirely happy with the layout and organization of the generated projects you can always [create your own templates to start from](../developer-tools.md#customizing-templates).

## Setting up Our Development Environment

Our generated project includes a `Makefile` with several helpers to streamline the development process. You can use these helpers, add your own, or do away with it and follow any other development process you are more familiar with.

First we will setup our VirtualENV:

```text
$ make virtualenv

$ source env/bin/activate

|> todo <| $
```

This runs common commands to create our virtual environment in `./env/`, and then runs `pip` to install our dependencies. We activate the environment, and are ready to run our TODO application:

```text
|> todo <| $ todo --help
usage: todo [-h] [-d] [-q] [-v]
            {command1} ...

A Simple TODO Application

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           full application debug mode
  -q, --quiet           suppress all console output
  -v, --version         show program's version number and exit

sub-commands:
  {command1}
    command1            example sub command1

Usage: todo command1 --foo bar
```

Look at that! Let's play around with some of the pre-built features:

```text
### display version information

$ todo --version
A Simple TODO Application 0.0.1.dev20180730022818
Cement Framework 3.0.0 
Python 3.7.0
Platform Darwin-17.7.0-x86_64-i386-64bit

### display sub-command help

$ todo command1 --help
usage: todo command1 [-h] [-f FOO]

optional arguments:
  -h, --help         show this help message and exit
  -f FOO, --foo FOO  notorious foo option

### execute the example command1 sub-command

$ todo command1 -f bar
Example Template (templates/command1.jinja2)
Foo => bar
```

## Conclusion

And that completes Part 1. In the next section we will add the functionality of managing task items, storing data in a database, and sending email messages when completing tasks.

