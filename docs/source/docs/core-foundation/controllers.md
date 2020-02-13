# Controllers

## Introduction to the Controller Interface

Cement defines a [Controller Interface](https://cement.readthedocs.io/en/3.0/api/core/controller/#cement.core.controller.ControllerInterface), but does not enable any handlers that implement the interface by default.

{% hint style="info" %}
For convenience, the preferred `ArgparseController` and `expose()` decorator from the [Argparse Extension](../extensions/argparse.md) are available as `Controller` and `ex` in the top level cement module.
{% endhint %}

Using application controllers is not necessary, but enables rapid development by wrapping pieces of the framework like adding arguments, and linking commands with controller methods. The examples below use the [`ArgparseController`](https://cement.readthedocs.io/en/3.0/api/ext/ext_argparse/#cement.ext.ext_argparse.ArgparseController) as examples \(again, imported as `cement.Controller` for convenience\).

{% hint style="warning" %}
Cement often includes multiple handler implementations of an interface that may or may not have additional features or functionality than the interface requires. The documentation below only references usage based on the interface and default handler \(not the full capabilities of an implementation\).
{% endhint %}

**Cement Extensions That Provide Controller Handlers**

* [Argparse](../extensions/argparse.md)

**API References:**

* [Cement Core Controller Module](https://cement.readthedocs.io/en/3.0/api/core/controller)
* [Cement Argparse Extension](https://cement.readthedocs.io/en/3.0/api/ext/ext_argparse)

## Application Base Controllers

When using application controllers there must be a single `base` controller responsible for handling [runtime dispatch](../terminology.md#runtime-dispatch). All other controllers are then [stacked](../terminology.md#controller-stacking) on top of the base controller \(or other controllers already stacked on base\). The base controller is the root of the application's command-line namespace.

{% hint style="info" %}
The initial base controller must have a `Controller.Meta.label` of `base` to designate it as the application's route of handing over runtime \(argument parsing, mapping sub-commands to controllers, etc\).

If no controller handler is registered with a `base` label, Cement will register a minimal controller in it's place that doesn't do anything other than allow extensions to stack properly.
{% endhint %}

{% tabs %}
{% tab title="Example: Defining an Application Base Controller" %}
```python
from cement import App, Controller, ex

class Base(Controller):
    class Meta:
        label = 'base'

    @ex(help='example sub-command')
    def cmd1(self):
        print('Inside Base.cmd1()')

class MyApp(App):
    class Meta:
        label = 'myapp'
        handlers = [
            Base,
        ]

with MyApp() as app:
    app.run()
```
{% endtab %}

{% tab title="cli" %}
```text
$ python myapp.py
usage: myapp [-h] [-d] [-q] {cmd1} ...

optional arguments:
  -h, --help   show this help message and exit
  -d, --debug  full application debug mode
  -q, --quiet  suppress all console output

sub-commands:
  {cmd1}
    cmd1       example sub-command

$ python myapp.py cmd1
Inside Base.cmd1()
```
{% endtab %}
{% endtabs %}

The above example demonstrates registering an application base controller. You will note in the `cli` tab that running `python myapp.py` without any arguments produces help output \(same as if passing `--help`\). This is the default action of the `ArgparseController`, but can be modified by overriding the `_default` method.

{% tabs %}
{% tab title="Example: Controller Default Method" %}
```python
from cement import App, Controller, ex

class Base(Controller):
    class Meta:
        label = 'base'

    def _default(self):
        print('Inside Base._default()')

    @ex(help='example sub-command')
    def cmd1(self):
        print('Inside Base.cmd1()')


class MyApp(App):
    class Meta:
        label = 'myapp'
        handlers = [
            Base,
        ]

with MyApp() as app:
    app.run()
```
{% endtab %}

{% tab title="cli" %}
```text
$ python myapp.py
Inside Base._default()
```
{% endtab %}
{% endtabs %}

{% hint style="info" %}
The `Controller._default` method is hidden from the command-line \(ex: `--help` output\), and does not require the `ex()` decorator to be active. You can modify the default method by setting it via `Controller.Meta.default_func`.
{% endhint %}

## Controller Arguments

Command line arguments defined by controllers are handled in two ways:

* Controller level
* Sub-command level

Controller level arguments are defined via `Controller.Meta.arguments` and are displayed/used at the top level of that controller, while sub-command level arguments are defined via the `ex()` decorator and only displayed and used under that sub-command namespace.

{% hint style="info" %}
Controller level arguments should be considered global, and relevant to the entire controller namespace. Sub-command level arguments are only relevant to that sub-command.
{% endhint %}

{% tabs %}
{% tab title="Example: Defining Controller Arguments" %}
```python
from cement import App, Controller, ex

class Base(Controller):
    class Meta:
        label = 'base'

        arguments = [
            ( [ '-f', '--foo' ],
              { 'help' : 'the notorious foo option',
                'action' : 'store',
                'dest' : 'foo', } ),
        ]

    @ex(
        help='example sub-command',
        arguments=[
            ( [ '--sub-option' ],
              { 'help' : 'option under sub-command',
                'action' : 'store_true',
                'dest' : 'sub_option' } ),
        ]
    )
    def cmd1(self):
        print('Inside Base.cmd1()')

        if self.app.pargs.foo is not None:
            print('Foo => %s' % self.app.pargs.foo)

        if self.app.pargs.sub_option is True:
            print('Sub Option Was Passed')


class MyApp(App):
    class Meta:
        label = 'myapp'
        handlers = [
            Base,
        ]

with MyApp() as app:
    app.run()
```
{% endtab %}

{% tab title="cli" %}
```text
$ python myapp.py --help
usage: myapp [-h] [-d] [-q] [-f FOO] {cmd1} ...

optional arguments:
  -h, --help         show this help message and exit
  -d, --debug        full application debug mode
  -q, --quiet        suppress all console output
  -f FOO, --foo FOO  the notorious foo option

sub-commands:
  {cmd1}
    cmd1             example sub-command


$ python myapp.py cmd1 --help
usage: myapp cmd1 [-h] [--sub-option]

optional arguments:
  -h, --help    show this help message and exit
  --sub-option  option under sub-command


$ python myapp.py -f bar cmd1 --sub-option
Inside Base.cmd1()
Foo => bar
Sub Option Was Passed
```
{% endtab %}
{% endtabs %}

{% hint style="warning" %}
How and where arguments are defined determines how they are used. An argument defined under a controller must be passed before any sub-command namespaces, otherwise the sub-parser will not recognize it and result in an `unrecognized argument error`.
{% endhint %}

## Processing Controller Level Arguments

In the above example we demonstrated accessing the controller level argument via `app.pargs.foo` in the `Base.cmd1()` method/sub-command. This worked fine. However, because controller level arguments should be considered global to the entire namespace, we should reduce duplicate code and handle controller level argument parsing in one place, regardless of what sub-command is passed.

The `ArgparseController` defines both a `_pre_argument_parsing` and`_post_argument_parsing` method for providing direct access to that controller's sub-parser \(`self._parser`\) and processing arguments. This is very similar to the `pre_argument_parsing` and `post_argument_parsing` [framework hooks](hooks.md#cement-framework-hooks), but local in scope to the controller.

{% tabs %}
{% tab title="Example: Processing Controller Level Arguments" %}
```python
from cement import App, Controller, ex

class Base(Controller):
    class Meta:
        label = 'base'

        arguments = [
            ( [ '-f', '--foo' ],
              { 'help' : 'the notorious foo option',
                'action' : 'store',
                'dest' : 'foo', } ),
        ]

    def _post_argument_parsing(self):
        if self.app.pargs.foo is not None:
            print('Foo => %s' % self.app.pargs.foo)

    @ex(help='example sub-command')
    def cmd1(self):
        print('Inside Base.cmd1()')

    @ex(help='another example sub-command')
    def cmd2(self):
        print('Inside Base.cmd2()')


class MyApp(App):
    class Meta:
        label = 'myapp'
        handlers = [
            Base,
        ]

with MyApp() as app:
    app.run()
```
{% endtab %}

{% tab title="cli" %}
```text
$ python myapp.py -f bar cmd1
Foo => bar
Inside Base.cmd1()

$ python myapp.py -f bar cmd2
Foo => bar
Inside Base.cmd2()
```
{% endtab %}
{% endtabs %}

## Additional Controllers and Namespaces

Any number of additional controllers can be added to your application after a base controller is registered. Additionally, these controllers can be `stacked` onto the base controller \(or any other controller\) in one of two ways:

* `embedded` - The controllers commands and arguments are included under the parent controller's name space.
* `nested` - The controller label is added as a sub-command under the parent controller's namespace \(effectively this is a sub-command with additional sub-sub-commands under it\)

For example, the `base` controller is accessed when calling `myapp.py` directly. Any commands under the `base` controller would be accessible as `myapp.py <cmd1>`, or `myapp.py <cmd2>`, etc. An `embedded` controller will merge its commands and options into the `base` controller namespace and appear to be part of the base controller... meaning you would still access the `embedded` controllers commands as `myapp.py <embedded_cmd1>`, etc \(same for options\).

For `nested` controllers, a prefix will be created with that controller's label under its parent's namespace. Therefore you would access that controller's commands and options as `myapp.py <controller_label> <controller_cmd1>`.

{% tabs %}
{% tab title="Example: Multiple Stacked Controllers" %}
```python
from cement import App, Controller, ex

class Base(Controller):
    class Meta:
        label = 'base'

    @ex(help='example sub-command')
    def cmd1(self):
        print('Inside Base.cmd1()')

class Embedded(Controller):
    class Meta:
        label = 'embedded'
        stacked_on = 'base'
        stacked_type = 'embedded'

    @ex(help='embedded sub-command')
    def cmd2(self):
        print('Inside Embedded.cmd2()')

class Nested(Controller):
    class Meta:
        label = 'nested'
        stacked_on = 'base'
        stacked_type = 'nested'

    @ex(help='nested sub-command')
    def cmd3(self):
        print('Inside Nested.cmd3()')

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
$ python myapp.py  --help
usage: myapp [-h] [-d] [-q] {nested,cmd1,cmd2} ...

optional arguments:
  -h, --help          show this help message and exit
  -d, --debug         full application debug mode
  -q, --quiet         suppress all console output

sub-commands:
  {nested,cmd1,cmd2}
    nested            nested controller
    cmd1              example sub-command
    cmd2              embedded sub-command


$ python myapp.py cmd1
Inside Base.cmd1()


$ python myapp.py cmd2
Inside Embedded.cmd2()


$ python myapp.py nested cmd3
Inside Nested.cmd3()
```
{% endtab %}
{% endtabs %}

{% hint style="info" %}
Controllers can be stacked on other controllers as many levels deep as necessary. An `embedded` controller can be stacked on top of a `nested` controller, and vice versa. There is little, if any, limitation.
{% endhint %}

