# Developer Tools

## Introduction

Cement ships with a CLI utility that includes tools and helpers for application developement. It is in-itself an application Built on Cement™, and can serve as a working example of some of the key features of the framework.

See: `$ cement --help`

The Cement CLI uses the builtin [Generate Extension](../extensions/generate.md) in order to easily create new projects, extensions, plugins, or scripts.

See `$ cement generate --help`

## Creating Your First Project Built on Cement™

Using the Cement Developer Tools CLI, you can quickly generate a new project:

_Note: Press_ `<ENTER>` _in order to take the default values for_ `myapp`_:_

```text
$ cement generate project ./myapp
INFO: Generating cement project in ./myapp
App Label [myapp]:
App Name [My Application]:
App Class Name [MyApp]:
App Description [MyApp Does Amazing Things!]:
Creator Name [John Doe]:
Creator Email [john.doe@example.com]:
Project URL [https://github.com/johndoe/myapp/]:
License [unlicensed]:
```

We have just generated a new project in the directory `./myapp`. The included `README.md` includes general information that is built-in to your new project out-of-the box including how to setup a development environment, run tests, push packages to PyPi, and deploy via Docker.

## Customizing Templates

The [Generate Extension](../extensions/generate.md) reads templates from any template directory paths, therefore adding your own templates to Cement is as simple as adding a template directory to Cement's configuration file, cloning a builtin template, and then generating from your own templates using the same utility.

Add the following to `~/.cement.yml`:

```text
cement:
    template_dir: ~/templates
```

Then clone an existing template:

```text
$ cement generate project \
    --clone ~/templates/generate/my-template
```

Your template is now part of Cement!  Customize it to your liking, and use it in the same way as the builtin templates:

```text
$ cement generate --help
usage: cement generate [-h]
                       {project,script,plugin,extension,my-template}
                       ...

optional arguments:
  -h, --help            show this help message and exit

sub-commands:
  {project,script,plugin,extension,my-template}
    project             generate project from template
    script              generate script from template
    plugin              generate plugin from template
    extension           generate extension from template
    my-template         generate my-template from template

```
