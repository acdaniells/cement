# Interfaces and Handlers

## Introduction to Interfaces

Cement builds upon a standard interface and handler system that is used
extensively to break up pieces of the framework into relatable chunks, and allow
customization of everything from logging to config file parsing, and almost
every operation in between.

.. note::
   In Cement, an interface is what **defines** some functionality, and a handler
   is what **implements** that functionality.

We call the implementation of an interface a **handler**, and provide the
ability to easily register and retrieve them via the `app.handler` object.
Cement interfaces are defined as [Python Abstract Base
Classes](https://docs.python.org/3/library/abc.html), and handlers implement
them by sub-classing and overriding the defined abstract methods required to
make the implementation legit.

**API References**

* [Cement Core Interface Module](https://cement.readthedocs.io/en/3.0/api/core/interface/)
* [Cement Core Handler Module](https://cement.readthedocs.io/en/3.0/api/core/handler/)

### Builtin Interfaces

The following interfaces are builtin to Cement's core foundation:

| **Interface** | **Description** |
| :--- | :--- |
| [**Extension**](extensions-1.md) | Framework extension loading. |
| [**Log**](https://cement.readthedocs.io/en/portland/api/core/log/#cement.core.log.LogHandler) | Messaging to console, and/or file via common log facilities \(INFO, WARNING, ERROR, FATAL, DEBUG\). |
| [**Config**](https://cement.readthedocs.io/en/portland/api/core/config/#cement.core.config.ConfigHandler) | Merging of application configuration defaults, configuration files, and environment settings into a single config object. |
| [**Mail**](https://cement.readthedocs.io/en/portland/api/core/mail/#cement.core.mail.MailHandler) | Remote message sending \(email, smtp, etc\). |
| [**Plugin**](https://cement.readthedocs.io/en/portland/api/core/plugin/#cement.core.plugin.PluginHandler) | Application plugin loading. |
| [**Template**](https://cement.readthedocs.io/en/portland/api/core/template/#cement.core.template.TemplateHandler) | Rendering of template data \(content, files, etc\). |
| [**Output**](https://cement.readthedocs.io/en/portland/api/core/output/#cement.core.output.OutputHandler) | Rendering of data/content to end-user output \(console text from template, JSON, Yaml, etc\).  Often uses an associated template handler backend. |
| [**Argument**](https://cement.readthedocs.io/en/portland/api/core/arg/#cement.core.arg.ArgumentHandler) | Command line argument/option parsing. |
| [**Controller**](https://cement.readthedocs.io/en/portland/api/core/controller/#cement.core.controller.ControllerHandler) | Command dispatch \(sub-commands, arguments, etc\) |
| [**Cache**](https://cement.readthedocs.io/en/portland/api/core/cache/#cement.core.cache.CacheHandler) | Key/Value data store \(memcached, redis, etc\) |

### Working With Interfaces

The [InterfaceManager](https://cement.readthedocs.io/en/3.0/api/core/interface/#cement.core.interface.InterfaceManager) \(`app.interface`\) provides quick mechanisms to list, get, and verify interfaces:

```python
from cement import App

with App('myapp') as app:
    # list defined interfaces
    app.interface.list()

    # get an interface class
    i = app.interface.get('output')

    # validate if an interface is defined
    app.interface.defined('mail')
```

### Defining an Interface

{% hint style="warning" %}
Defining interfaces is more of an advanced topic, and is not required to fully grasp for new developers or those new to the framework.
{% endhint %}

Cement uses interfaces and handlers extensively to manage the framework, however developers can also make use of this system to provide a clean, and standardized way of allowing other developers to customize their application \(generally via application plugins\).

The following defines a basic interface we'll call `greeting`:

```python
from abc import abstractmethod
from cement import App, Interface

​class GreetingInterface(Interface):
    class Meta:
        interface = 'greeting'

    @abstractmethod
    def _get_greeting(self):
        """
        Get a greeting message for the end-user.

        Returns:
            greeting (str): The greeting string to present to
                the end-user.
        """
        pass

    @abstractmethod
    def greet(self):
        """
        Display a greeting message for the end-user.

        Returns: None
        """
        pass

class MyApp(App):
    label = 'myapp'
    interfaces = [
        GreetingInterface,
    ]
```

The above example defines the `greeting` interface, by providing abstract methods that any handlers implementing this interface must provide. It does not implement any functionality on its own \(though it could\), but rather defines and documents its purpose and its expected implementation. The interface is easily defined with the framework by listing it in `App.Meta.interfaces`, but you can also define interfaces directly with `app.interface.define()`.

### Implementing an Interface

In order to implement the above `greeting` interface, we first want to provide a handler base class that will be the starting point for all implementations that sub-class from it:

```python
from cement import Handler

class GreetingHandler(GreetingInterface, Handler):

    def greet(self):
        self.app.log.debug('about to greet end-user')
        msg = self._get_greeting()
        assert isinstance(str, msg), "The msg is not a string!"
        print(msg)
```

{% hint style="info" %}
Handler base classes sub-class from both the interface they are implementing \(`GreetingInterface`\), and also the Cement Handler base class \(`Handler`\). The application developer defining the interface should always provide a handler base class for the implementation, even if the base class does not fully satisfy the interface.
{% endhint %}

In the above example, the developer would call the `greet()` method that will do all of the common operations like logging, exception handling, etc for all implementations, leaving only the minimal `_get_greeting()` method to be provided by the final implementation sub-classes. This follows the common [Don't Repeat Yourself \(DRY\)](https://en.wikipedia.org/wiki/Don't_repeat_yourself) principle's best practice \(all-be-it a tediously simple example\), where all of the reusable logic can live in one place, and sub-classes only focus on their unique means of implementing an interface.

In order to complete our implementation of the above `greeting` interface, we can now sub-class from the provided `GreetingHandler` base class, and fill in the missing pieces:

```python
class Hello(GreetingHandler):
    class Meta:
        label = 'hello'

    def _get_greeting(self):
        return 'Hello!'


class Goodbye(GreetingHandler):
    class Meta:
        label = 'goodbye'

    def _get_greeting(self):
        return 'Goodbye!'
```

{% hint style="info" %}
An interface defines itself to the framework via the `Interface.Meta.interface` string, and a handler defines itself via the `Handler.Meta.label` string. Collectively, all implementation handlers are referred to by both as `<interface>.<label>` or in the above examples `greeting.hello` and `greeting.goodbye`.
{% endhint %}

### Putting It All Together

The following is an [MCVE](../terminology.md#minimal-complete-verifiable-example-mcve) of defining an interface, providing an implementation handler base class, and registering multiple handlers that implement the interface differently:

{% tabs %}
{% tab title="myapp.py" %}
```python
from abc import abstractmethod
from cement import App, Interface, Handler

class GreetingInterface(Interface):
    class Meta:
        interface = 'greeting'

    @abstractmethod
    def _get_greeting(self):
        """
        Get a greeting message for the end-user.

        Returns:
            greeting (str): The greeting string to present to
                the end-user.
        """
        pass

    @abstractmethod
    def greet(self):
        """
        Display a greeting message for the end-user.

        Returns: None
        """
        pass


class GreetingHandler(GreetingInterface, Handler):

    def greet(self):
        self.app.log.debug('about to greet end-user')
        msg = self._get_greeting()
        assert isinstance(msg, str), "The msg is not a string!"
        print(msg)


class Hello(GreetingHandler):
    class Meta:
        label = 'hello'

    def _get_greeting(self):
        return 'Hello!'


class Goodbye(GreetingHandler):
    class Meta:
        label = 'goodbye'

    def _get_greeting(self):
        return 'Goodbye!'


class MyApp(App):
    class Meta:
        label = 'myapp'

        interfaces = [
            GreetingInterface,
        ]

        handlers = [
            Hello,
            Goodbye,
        ]

with MyApp() as app:
    app.run()
    g = app.handler.get('greeting', 'hello', setup=True)
    g.greet()
```
{% endtab %}

{% tab title="cli" %}
```text
$ python myapp.py
Hello!

$ python myapp.py -l debug
2018-07-17 20:28:21,449 (DEBUG) myapp : about to greet end-user
Hello!
```
{% endtab %}
{% endtabs %}

## Introduction to Handlers

Where an interface defines what an implementation is expected to provide, a handler is what actually implements the interface.

### Working with Handlers

The [HandlerManager](https://cement.readthedocs.io/en/3.0/api/core/handler/#cement.core.handler.HandlerManager) \(`app.handler`\) provides quick mechanisms to list, get, resolve and verify handlers. The following are a few examples of working with handlers:

```python
from cement import App

​with App('myapp') as app:
    # get a log handler called logging
    lh = app.handler.get('log', 'logging', setup=True)​

    # List all handlers registered to the config interface
    app.handler.list('config')​

    # check if the handler argparse is registered
    # to the argument interface
    app.handler.registered('argument', 'argparse')

    # resolve a handler by string, class, or object
    app.handler.resolve('log', 'logging')
    app.handler.resolve('log', LoggingLogHandler)
    app.handler.resolve('log', LoggingLogHandler())
```

{% hint style="info" %}
It is important to note that handlers are stored within the application as uninstantiated objects. Meaning you must instantiate them after retrieval \(call `_setup(app)`\) or simply pass `setup=True` to the `app.handler.get()` method.
{% endhint %}

### Registering Handlers to an Interface

An interface simply defines what an implementation is expected to provide, whereas a handler actually implements the interface.

{% tabs %}
{% tab title="Registering a Handler to an Interface" %}
The following is a simple example of sub-classing an existing handler, then registering that with the framework.

```python
from cement import App
from cement.ext.ext_configparser import ConfigParserConfigHandler

class MyConfigHandler(ConfigParserConfigHandler):
    class Meta:
        label = 'my_config_handler'

    # do something to sub-class ConfigParserConfigHandler

class MyApp(App):
    class Meta:
        label = 'myapp'
        handlers = [MyConfigHandler]
```
{% endtab %}
{% endtabs %}

### Overriding Default Handlers <a id="overriding-default-handlers"></a>

Cement sets up a number of default handlers for logging, config parsing, etc. These can be overridden in a number of ways, however the primary method is to override their associated setting in [App.Meta](https://cement.readthedocs.io/en/3.0/api/core/foundation/#cement.core.foundation.App.Meta).

{% tabs %}
{% tab title="Overriding Default Handlers" %}
Using the above `MyConfigHandler` example, we simply need to register a handler to an interface, and then override the `App.Meta.config_handler` option:

```python
class MyApp(App):
    class Meta:
        label = 'myapp'
        handlers = [MyConfigHandler]
        config_handler = 'my_config_handler'
```
{% endtab %}
{% endtabs %}

All builtin core interfaces have an associated `App.Meta.x_handler` option, allowing complete customization of every aspect of the framework. See the reference documentation of [App.Meta](https://cement.readthedocs.io/en/3.0/api/core/foundation/#cement.core.foundation.App.Meta) for more detail.

### Multiple Registered Handlers <a id="multiple-registered-handlers"></a>

All handlers and interfaces are unique. In most cases, where the framework is concerned, only one handler is used. For example, whatever is configured for the [`App.Meta.log_handler`](https://cement.readthedocs.io/en/3.0/api/core/foundation/#cement.core.foundation.App.Meta.log_handler) will be used and setup as `app.log`. However, take for example an Output Handler. You might have a default [`App.Meta.output_handler`](https://cement.readthedocs.io/en/3.0/api/core/foundation/#cement.core.foundation.App.Meta.output_handler) of `mustache` \(a text templating language\) but may also want to override that handler with the `json` output handler when `-o json` is passed at command line. In order to allow this functionality, both the `mustache` and `json` output handlers must be registered.

Any number of handlers can be registered to an interface. You might have a use case for an Interface/Handler that may provide different compatibility based on the operating system, or perhaps based on simply how the application is called. A good example would be an application that automates building packages for Linux distributions. An interface would define what a build handler needs to provide, but the build handler would be different based on the OS. The application might have an `rpm` build handler, or a `dpkg` build handler to perform the build process differently.

### Customizing Handler Configuration and Meta <a id="customizing-handlers"></a>

Depending on the handler, you will have different ways of customizing its functionality. Some handlers honor application configuration setting, while others may only rely on meta-options. In either case, both can be modified at the top level of your application meta.

In the following example, we modify the configuration _defaults_ of the log handler, and also the meta-options to enable an optional log level command line argument feature it supports.

{% hint style="warning" %}
Note that configuration settings are always overridable via configuration files, however this example is modifying the builtin default setting of the log handler.
{% endhint %}

{% tabs %}
{% tab title="Example: Customizing Handler Configuration and Meta" %}
```python
from cement import App, init_defaults

CONFIG = init_defaults('myapp', 'log.logging')
CONFIG['log.logging']['level'] = 'warning'

META = init_defaults('log.logging')
META['log.logging']['log_level_argument'] = ['-l', '--level']

class MyApp(App):
    class Meta:
        label = 'myapp'
        config_defaults = CONFIG
        meta_defaults = META
```
{% endtab %}
{% endtabs %}

{% hint style="info" %}
If modifying the configuration or meta options isn't enough, you can always sub-class an existing handler and register your own in its place.
{% endhint %}

### Overriding Handlers via Command Line <a id="overriding-handlers-via-command-line"></a>

In some use cases, you will want the end user to have access to override the default handler of a particular interface. For example, Cement ships with multiple Output Handlers including `json`, `yaml`, and `mustache`. A typical application might default to using `mustache` to render console output from text templates. That said, without changing any code in the application, the end user could simply pass the `-o json` command line option and output the same data that is rendered to template, out in pure JSON.

{% hint style="warning" %}
Output hander overrides are not enabled by default, but can be enabled by setting the `OutputHandler.Meta.overridable` option to `True` for the output handlers that you want overridable by the `-o` option at command line. See the documentation on [Output Rendering](output-rendering.md) for more details and examples.
{% endhint %}

The only built-in handler override that Cement includes is for the above mentioned JSON example, but you can add any that your application requires.

{% tabs %}
{% tab title="Example: Overriding Handlers via Command Line" %}
{% code-tabs %}
{% code-tabs-item title="myapp.py" %}
```python
from cement import App, init_defaults

META = init_defaults('output.json', 'output.yaml')
META['output.json']['overridable'] = True
META['output.yaml']['overridable'] = True

class MyApp(App):
    class Meta:
        label = 'myapp'
        extensions = ['json', 'yaml', 'mustache']
        meta_defaults = META
        output_handler = 'mustache'
        template_dir = './templates'

with MyApp() as app:
    app.run()

    data = {'foo': 'bar'}
    app.render(data, 'example.m')
```
{% endcode-tabs-item %}

{% code-tabs-item title="templates/example.m" %}
```text
Foo: {{ foo }}
```
{% endcode-tabs-item %}
{% endcode-tabs %}
{% endtab %}

{% tab title="cli" %}
```text
$ python myapp.py --help
usage: myapp [-h] [-d] [-q] [-o {json,yaml}]

optional arguments:
  -h, --help      show this help message and exit
  -d, --debug     full application debug mode
  -q, --quiet     suppress all console output
  -o {json,yaml}  output handler

$ python myapp.py
Foo: bar

$ python myapp.py -o json
{"foo": "bar"}

$ python myapp.py -o yaml
foo: bar
```
{% endtab %}
{% endtabs %}

Notice the `-o` command line option, that includes the choices: `yaml` and `json`. This feature will include all Output Handlers that have the `overridable` meta-data option set to `True`. We did not set this option for the mustache handler, therefore it did not show up as a choice for the `-o` option at command-line.

