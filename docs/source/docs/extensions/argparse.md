# Argparse

## Introduction

The Argparse Extension provides the [`ArgparseArgumentHandler`](http://cement.readthedocs.io/en/3.0/api/ext/ext_argparse/#cement.ext.ext_argparse.ArgparseArgumentHandler) for argument parsing, and the [`ArgparseController`](http://cement.readthedocs.io/en/3.0/api/ext/ext_argparse/#cement.ext.ext_argparse.ArgparseController) for runtime dispatch. Both are the defaults used by Cement.

**Documentation References:**

* [Arguments](../core-foundation/arguments.md)
* [Controllers](../core-foundation/controllers.md)

**API References**

* [Cement Argparse Extension](http://cement.readthedocs.io/en/3.0/api/ext/ext_argparse/)
* [Python Argparse Module](https://docs.python.org/3/library/argparse.html)

## Requirements

* Python 2.7+, 3+
* Some features of ArgparseController are only available in Python 3 including controller and function/command aliases \(Python 3+\) and controller default functions/commands \(Python 3.4+\).

## Configuration

This extension does not rely on any application level configuration settings or meta options.

## Usage

The following is an example application using both the [`ArgparseArgumentHandler`](http://cement.readthedocs.io/en/3.0/api/ext/ext_argparse/#cement.ext.ext_argparse.ArgparseArgumentHandler) and [`ArgparseController`](http://cement.readthedocs.io/en/3.0/api/ext/ext_argparse/#cement.ext.ext_argparse.ArgparseController). Note that the default `arg_handler` is already set to`ArgparseArgumentHandler` by `App`.

{% tabs %}
{% tab title="Example: Using Argparse Extension" %}
```python
from cement import App, Controller, ex

class Base(Controller):
    class Meta:
        label = 'base'
        arguments = [
            (['--base-foo'],
             {'help': 'base foo option'}),
        ]

    @ex(hide=True)
    def default(self):
        print('Inside Base.default')

        if self.app.pargs.base_foo:
            # do something with self.app.pargs.base_foo
            print('Base Foo > %s' % self.app.pargs.base_foo)

    @ex(
        arguments=[
            (['--command1-opt'],
             {'help': 'option under command1',
              'action': 'store_true'})
        ],
        aliases=['cmd1'],
        help='sub-command under myapp base controller',
    )
    def command1(self):
        print('Inside Base.command1')

        if self.app.pargs.command1_opt:
            # do something with self.app.pargs.command1_opt
            pass

class Embedded(Controller):
    class Meta:
        label = 'embedded_controller'
        stacked_on = 'base'
        stacked_type = 'embedded'

    @expose(help="embedded under base controller")
    def command2(self):
        print('Inside Embedded.command2')

class Nested(Controller):
    class Meta:
        label = 'nested_controller'
        stacked_on = 'base'
        stacked_type = 'nested'
        arguments = [
            (['--nested-opt'],
             {'help': 'option under nested-controller'}),
        ]

    @expose(help="sub-command under nested-controller")
    def command3(self):
        print('Inside Nested.command3')

class MyApp(App):
    class Meta:
        label = 'myapp'
        handlers = [
            Base,
            Embedded,
            Nested,
        ]

with MyApp() as app:
    app.run()
```
{% endtab %}

{% tab title="cli" %}
```text
$ python myapp.py --help
usage: myapp.py [-h] [--quiet] [--base-foo BASE_FOO]
                {nested-controller,command1,cmd1,default,command2} ...

optional arguments:
  -h, --help            show this help message and exit
  --quiet               suppress all output
  --base-foo BASE_FOO   base foo option

sub-commands:
  {nested-controller,command1,cmd1,default,command2}
    nested-controller   nested-controller controller
    command1 (cmd1)     command1 is a sub-command under base controller
    command2            command2 embedded under base controller


$ python myapp.py --base-foo bar
Inside Base.default
Base Foo > bar


$ python myapp.py command1 --help
usage: myapp.py command1 [-h] [--command1-opt]

optional arguments:
  -h, --help      show this help message and exit
  --command1-opt  option under command1


$ python myapp.py command1
Inside Base.command1


$ python myapp.py command2
Inside Embedded.command2


$ python myapp.py nested-controller --help
usage: myapp.py nested-controller [-h] [--nested-opt] {command3} ...

optional arguments:
  -h, --help            show this help message and exit
  --nested-opt          option under nested-controller

sub-commands:
  {command3}
    command3            command3 under nested-controller


$ python myapp.py nested-controller command3
Inside Nested.command3
```
{% endtab %}
{% endtabs %}

