# Arguments

## Introduction to the Argument Interface

Cement defines an [Argument Interface](https://cement.readthedocs.io/en/3.0/api/core/arg/#cement.core.arg.ArgumentInterface), as well as the default [ArgParseArgumentHandler](https://cement.readthedocs.io/en/3.0/api/core/arg/#cement.core.arg.ArgumentHandler) that implements the interface. This handler is built on top of the [ArgParse](http://docs.python.org/library/argparse.html) module which is included in the Python standard library.

{% hint style="warning" %}
Cement often includes multiple handler implementations of an interface that may or may not have additional features or functionality than the interface requires. The documentation below only references usage based on the interface and default handler \(not the full capabilities of an implementation\).
{% endhint %}

**Cement Extensions That Provide Argument Handlers:**

* [Argparse](../extensions/argparse.md)

**API References:**

* [Cement Core Argument Module](https://cement.readthedocs.io/en/3.0/api/core/arg/)
* [Cement Argparse Extension](https://cement.readthedocs.io/en/3.0/api/ext/ext_argparse)

## **Configuration**

### **Application Meta Options**

The following options under [`App.Meta`](https://cement.readthedocs.io/en/3.0/api/core/foundation/#cement.core.foundation.App.Meta) modify configuration handling:

| **Option** | **Description** |
| :--- | :--- |
| **arg\_handler** | The handler that implements the argument interface. |

## Adding Arguments

The argument interface is loosely based on Argparse, but only defines a minimal set of params that must be honored as to ensure that the framework and extensions can add arguments regardless of what the argument handler implementation is. That said, Cement has never intended to use anything other than Argparse to handle arguments and for that reason there may be some assumptions inherently builtin that assume the underlying argument handler is 100% argparse compliant. For that reason, adding and working with arguments will be completely familiar for anyone who has ever used Argparse.

{% tabs %}
{% tab title="Example: Adding Arguments" %}
```python
from cement import App

with App('myapp') as app:
    # add arguments before app.run()
    app.args.add_argument('-f', '--foo', 
                          action='store', 
                          dest='foo')                     

    # run the application (parses arguments)
    app.run()
```
{% endtab %}

{% tab title="cli" %}
```text
$ python myapp.py --help
usage: myapp [-h] [-d] [-q] [-f FOO]

optional arguments:
  -h, --help         show this help message and exit
  -d, --debug        full application debug mode
  -q, --quiet        suppress all console output
  -f FOO, --foo FOO
```
{% endtab %}
{% endtabs %}

## Accessing Parsed Arguments

During `app.run()`, command line arguments are parsed by the argument handler, and the results are stored by the application. Arguments are then accessible by [`App.pargs`](https://cement.readthedocs.io/en/3.0/api/core/foundation/#cement.core.foundation.App.pargs) \(parsed args\).

{% tabs %}
{% tab title="Example: Accessing Parsed Arguments" %}
```python
from cement import App

with App('myapp') as app:
    # add arguments before app.run()
    app.args.add_argument('-f', '--foo', 
                          action='store', 
                          dest='foo')                     

    # run the application (parses arguments)
    app.run()

    # test if argument was passed
    if app.pargs.foo is not None:
        print('Foo => %s ' app.pargs.foo
```
{% endtab %}
{% endtabs %}

## Creating an Argument Handler

All interfaces in Cement can be overridden with your own implementation. This can be done either by sub-classing [ArgumentHandler](https://cement.readthedocs.io/en/3.0/api/core/template/#cement.core.template.TemplateHandler) itself, or by sub-classing an existing extension's handlers in order to alter their functionality.

{% tabs %}
{% tab title="Example: Creating an Argument Handler" %}
{% code-tabs %}
{% code-tabs-item title="myapp.py" %}
```python
from cement import App
from cement.core.arg import ArgumentHandler

class MyArgumentHandler(ArgumentHandler):
    class Meta:
        label = 'my_argument_handler'

    # do something to implement the interface

class MyApp(App):
    class Meta:
        label = 'myapp'
        argument_handler = 'my_argument_handler'
        handlers = [
            MyArgumentHandler,
        ]
```
{% endcode-tabs-item %}
{% endcode-tabs %}
{% endtab %}
{% endtabs %}

