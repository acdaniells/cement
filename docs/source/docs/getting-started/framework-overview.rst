Framework Overview
==================

This section is intended to give a brief overview of some of the most commonly
used core features of Cement. Please do not be discouraged if you don't "get it"
right away. Please also do not think, "is this it?". This is not intended to be
an exhaustive end-all-be-all coverage of every feature of the framework.

Some assumptions are being made here. Primarily, we assume that you've used and
are familiar with Python. The overview is intended to give a high level look at
using Cement. Please dive deeper into the individual sections after the overview
in order to gain a better understanding of each component.

The Application Object
----------------------

The core of your project starts with the Cement ``App`` object, which we will
refer to throughout this documentation in several ways:

-  ``App`` - The uninstantiated Cement ``App`` base class
-  ``MyApp`` - The uninstatiated/sub-classed Cement application you are creating
-  ``app`` - The instantiated application object

Technically, Cement ``App`` can be used direcly (as in the example), however in
practice you will almost always sub-class ``App`` in order to configure it for
your needs (i.e. ``MyApp``).

.. code:: python
   :linenos:
   :caption: Using App Directly
   :name: using-app-directly

    from cement import App

    with App('myapp') as app:
        app.run()

.. code:: python
   :linenos:
   :caption: Subclassing App
   :name: subclassing-app

    from cement import App

    class MyApp(App):
        class Meta:
            label = 'myapp'

    with MyApp() as app:
        app.run()

.. code:: text
   :caption: Usage
   :name: usage

    $ python myapp.py --help
    usage: myapp [-h] [--debug] [--quiet]

    optional arguments:
      -h, --help  show this help message and exit
      --debug     toggle debug output
      --quiet     suppress all output

MetaMixin
---------

Cement uses ``MetaMixin`` classes everywhere, which allows the framework to
define default functionality but also provides an easy mechanism for developers
to override and customize.

This is implemented by declaring a ``Meta`` class, under your application and/or
other Cement Handler classes.

.. code:: python
   :linenos:
   :caption: **Example:** Defining Meta Classes
   :name: example-defining-meta-classes

    from cement import App

    class MyApp(App):
        class Meta:
            label = 'myapp'
            extensions = ['json']

All Meta-options can also be overridden by any ``**kwargs`` that are passed to
the parent class that is being instantiated.

.. code:: python
   :linenos:
   :caption: **Example:** Passing meta options via ``**kwargs``
   :name: example-passing-meta-options-via-kwargs

    App('myapp', config_defaults={'foo': 'bar'})

Nearly every Cement class has an associated ``Meta`` class, which we often refer
to as ``App.Meta``, ``SomeHandlerClass.Meta``, etc. The instantiated object is
refered to in code as ``app._meta``, ``some_handler._meta``, etc.

Interfaces and Handlers
-----------------------

All aspects of the framework are broken up into interfaces, and handlers.
Interfaces **define** some functionality, while handlers **implement** that
functionality. Cement defines the following builtin core interfaces:

+----------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------+
| Interface                                                                                                                                    | Descripton                                                                                                                                       |
+==============================================================================================================================================+==================================================================================================================================================+
| `**Extension** <../core-foundation/extensions-1.md>`__                                                                                       | Framework extension loading.                                                                                                                     |
+----------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------+
| **​**\ `**Log** <https://cement.readthedocs.io/en/portland/api/core/log/#cement.core.log.LogHandler>`__\ **​**                               | Messaging to console, and/or file via common log facilities (INFO, WARNING, ERROR, CRITICAL, DEBUG).                                                |
+----------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------+
| **​**\ `**Config** <https://cement.readthedocs.io/en/portland/api/core/config/#cement.core.config.ConfigHandler>`__\ **​**                   | Merging of application configuration defaults, configuration files, and environment settings into a single config object.                        |
+----------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------+
| **​**\ `**Mail** <https://cement.readthedocs.io/en/portland/api/core/mail/#cement.core.mail.MailHandler>`__\ **​**                           | Remote message sending (email, smtp, etc).                                                                                                       |
+----------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------+
| **​**\ `**Plugin** <https://cement.readthedocs.io/en/portland/api/core/plugin/#cement.core.plugin.PluginHandler>`__\ **​**                   | Application plugin loading.                                                                                                                      |
+----------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------+
| **​**\ `**Template** <https://cement.readthedocs.io/en/portland/api/core/template/#cement.core.template.TemplateHandler>`__\ **​**           | Rendering of template data (content, files, etc).                                                                                                |
+----------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------+
| **​**\ `**Output** <https://cement.readthedocs.io/en/portland/api/core/output/#cement.core.output.OutputHandler>`__\ **​**                   | Rendering of data/content to end-user output (console text from template, JSON, Yaml, etc). Often uses an associated template handler backend.   |
+----------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------+
| **​**\ `**Argument** <https://cement.readthedocs.io/en/portland/api/core/arg/#cement.core.arg.ArgumentHandler>`__\ **​**                     | Command line argument/option parsing.                                                                                                            |
+----------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------+
| **​**\ `**Controller** <https://cement.readthedocs.io/en/portland/api/core/controller/#cement.core.controller.ControllerHandler>`__\ **​**   | Command dispatch (sub-commands, arguments, etc)                                                                                                  |
+----------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------+
| **​**\ `**Cache** <https://cement.readthedocs.io/en/portland/api/core/cache/#cement.core.cache.CacheHandler>`__\ **​**                       | Key/Value data store (memcached, redis, etc)                                                                                                     |
+----------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------+

To accompany the above interfaces, Cement also defines and registers default
Handlers that implement the required functionality. For example, the builtin
configuration handler ``ConfigParserConfigHandler``, implements the ``config``
interface.

.. note::
   Handlers are referred to by the interfaces they implement, such as
   ``config.configparser``, ``config.json``, ``config.yaml``, etc. Application
   developers can also define their own interfaces, allowing customization by
   plugins.

Developers can override the default functionality by creating their own
handlers, or by sub-classing what is provided to alter its implementation. The
following example demonstrates how you would sub-class and override an existing
handler:

.. code:: python
   :linenos:
   :caption: **Example:** Overriding Default Framework Handlers
   :name: example-overriding-default-framework-handlers

    from cement import App
    from cement.ext.ext_configparser import ConfigParserConfigHandler


    class MyConfigHandler(ConfigParserConfigHandler):
        class Meta:
            label = 'my_config_handler'

        # do something to subclass/re-implement
        # config handler here...


    class MyApp(App):
        class Meta:
            label = 'myapp'
            config_handler = 'my_config_handler'
            handlers = [MyConfigHandler]

**Overriding Via Configuration Files**

The ``App.Meta`` options define the builtin handlers for all of the above listed
core handlers. Whatever the application code defines is the default, however you
can also override via the configuration file(s).

For example, imagine that your default ``mail_handler`` is ``smtp`` for sending
email via your local SMTP server. This is a configuration that might vary on a
per-user/environment basis. Via the application configuration, you could
override this with an alternative mail handler like ``mail_handler =
some_other_mail_handler``

.. code:: text
   :caption: **Example:** Overriding Via Configuration File - ~/.myapp.conf
   :name: example-overriding-via-configuration-file

    [myapp]

    ### override App.Meta.mail_handler
    mail_handler = my_mail_handler

Configuration
-------------

Cement supports loading multiple configuration files out-of-the-box.
Configurations loaded from files are merged in, overriding the
applications default settings (``App.Meta.config_defaults``). The
default configuration handler is ``ConfigParserConfigHandler``, based on
`ConfigParser <https://docs.python.org/3/library/configparser.html>`__
in the standard library, and is instantiated as ``app.config``.

Cement looks for configuration files in the most common places by
default. For example:

-  /etc/myapp/myapp.yml
-  ~/.config/myapp/myapp.yml
-  ~/.config/myapp/config
-  ~/.config/myapp.yml
-  ~/.myapp.yml
-  ~/.myapp/config

The list of configuration file paths can be customized via the meta
option
```App.Meta.config_files`` <https://cement.readthedocs.io/en/portland/api/core/foundation/#cement.core.foundation.App.Meta.config_files>`__
as well as their extension (i.e. ``.conf``) can also be easily modified
with
```App.Meta.config_file_suffix`` <https://cement.readthedocs.io/en/portland/api/core/foundation/#cement.core.foundation.App.Meta.config_file_suffix>`__.

The builtin configuration handler ``ConfigParserConfigHandler`` uses
common unix-like config files where ``blocks`` or ``sections`` are
defined with brackets; ``[myapp]``, ``[plugin.myplugin]``,
``[interface.handler]``, etc.

Additional support for the following file formats is provided via
optional extensions:

-  `Json <../extensions/json.md>`__
-  `Yaml <../extensions/yaml.md>`__

.. note::
   Config handler's provide dropin replacements for
   the default ConfigParserConfigHandler, and are often based on it. For
   example, the JsonConfigHandler and YamlConfigHandler classes do little
   more than support reading alternative file formats. Accessing the config
   settings in the app is exactly the same.

All extensions and application plugins can support customizations loaded
from the application configuration files under the section
``[interface.handler]``. For example, the ``ColorLogHandler`` extension
reads it's configuration from ``[log.colorlog]``.

Ex: Application Configuration Settings

{% tabs %} {% tab title="myapp.py" %}

.. code:: python

    from cement import App, init_defaults

    defaults = init_defaults('myapp')
    defaults['myapp']['foo'] = 'bar'

    class MyApp(App):
        class Meta:
            label = 'myapp'
            config_defaults = defaults

    with MyApp() as app:
        app.run()
        print("Foo => %s" % app.config.get('myapp', 'foo'))

{% endtab %}

{% tab title="~/.myapp.conf" %}

.. code:: text

    [myapp]
    foo = not-bar

{% endtab %}

{% tab title="cli" %}

.. code:: text

    $ python myapp.py
    Foo => not-bar

{% endtab %} {% endtabs %}

**Alternative Configuration Handler Example**

The following is an example of overriding the default config handler
with an alternative, drop-in replacement ``YamlConfighandler``:

Ex: Alternative Configuration Handler (Yaml):

{% tabs %} {% tab title="myapp.py" %}

.. code:: python

    from cement import App

    class MyApp(App):
        class Meta:
            label = 'myapp'
            extensions = ['yaml']
            config_handler = 'yaml'
            config_file_suffix = '.yml'

{% endtab %}

{% tab title="~/.myapp.yml" %}

.. code:: yaml

    myapp:
        foo: not-bar

{% endtab %} {% endtabs %}

**Overriding Configuration Settings with Environment Variables**

All configuration settings can be overridden by their associated
environment variables. For example ``config['myapp']['foo']`` is
overridable by ``$MYAPP_FOO``.

Note that all environment variable configurations are prefixed with the
application label, therefore secondary namespaces such as
``config['log.logging']['level']`` would be overridable by
``MYAPP_LOG_LOGGING_LEVEL``.

Arguments
---------

Argument parsing is based on the standard
`Argparse <https://docs.python.org/3/library/argparse.html>`__ library,
with the same usage that you're familiar with. The argument handler
``ArgparseArgumentHandler`` is instantiated as ``app.args``, arguments
are defined with ``app.args.add_argument()``, and parsed arguments are
stored as ``app.args.parsed_args`` (or more conveniently ``app.pargs``
for easy reference).

Ex: Simple Arguments Defined With Cement App

{% tabs %} {% tab title="myapp.py" %}

.. code:: python

    from cement import App

    with App('myapp') as app:
        app.args.add_argument('-f', '--foo',
                              help='notorous foo option',
                              dest='foo')
        app.run()

        # do something with parsed arguments
        if app.pargs.foo is not None:
            print("Foo Argument => %s" % app.pargs.foo)

{% endtab %}

{% tab title="cli" %}

.. code:: text

    $ python myapp.py --help
    usage: myapp [-h] [--debug] [--quiet] [-f FOO]

    optional arguments:
      -h, --help         show this help message and exit
      --debug            toggle debug output
      --quiet            suppress all output
      -f FOO, --foo FOO  notorous foo option

    $ python myapp.py -f bar
    Foo Argument => bar

{% endtab %} {% endtabs %}

**Arguments Defined by Controllers**

The power of the framework comes into play when we start talking about
application controllers that streamline the process of mapping arguments
and sub-commands to actions/functions as in the example (more on this
later).

Ex: Arguments Defined by Controllers

{% tabs %} {% tab title="myapp.py" %}

.. code:: python

    from cement import App, Controller, ex


    class Base(Controller):
        class Meta:
            label = 'base'

            arguments = [
                # list of tuples in the format `( [], {} )`
                ( [ '-f', '--foo' ],
                  { 'help' : 'notorious foo option',
                    'dest' : 'foo' } ),
            ]

        @ex(hide=True)
        def _default(self):
            print('Inside BaseController._default()')

            # do something with parsed arguments
            if self.app.pargs.foo is not None:
                print("Foo Argument => %s" % self.app.pargs.foo)


    class MyApp(App):
        class Meta:
            label = 'myapp'
            handlers = [Base]


    with MyApp() as app:
        app.run()

{% endtab %}

{% tab title="cli" %}

.. code:: text

    $ python myapp.py --help
    usage: myapp [-h] [--debug] [--quiet] [-f FOO]

    optional arguments:
      -h, --help         show this help message and exit
      --debug            toggle debug output
      --quiet            suppress all output
      -f FOO, --foo FOO  notorous foo option

    $ python myapp.py -f bar
    Foo Argument => bar

{% endtab %} {% endtabs %}

Logging
-------

Logging is based on the standard
`Logging <https://docs.python.org/3/library/logging.html>`__ library,
with the same usage you're familiar with. The logging facility is
customizable via the ``[log.logging]`` section of an applications
configuration:

-  ``level`` - The level at which to start logging (``INFO``,
   ``WARNING``, ``ERROR``,

``FATAL``, ``DEBUG``, etc).

-  ``file`` (*path*) - File path to log to.
-  ``to_console`` (*bool*) - Whether or not to log to console.
-  ``rotate`` (*bool*) - Whether or not to rotate the log file when it
   hits

``max_bytes``

-  ``max_bytes`` (*int*) - Maximum file size in bytes before file gets
   rotated
-  ``max_files`` (*int*) - Maximum number of log files to keep after
   rotating

Cement also includes the following optional extensions that provide
drop-in replacements for the default log handler:

-  `ColorlogHandler <../extensions/colorlog.md>`__ - Provides colorized
   log output via the
   `Colorlog <https://github.com/borntyping/python-colorlog>`__ library.

Ex: Logging Example

{% tabs %} {% tab title="myapp.py" %}

.. code:: python

    from cement import App

    with App('myapp') as app:
        app.run()

        # log messages to console and file
        app.log.info('this is an info message')
        app.log.warning('this is an warning message')
        app.log.error('this is an error message')
        app.log.fatal('this is an fatal message')
        app.log.debug('this is an debug message')

{% endtab %}

{% tab title="~/.myapp.conf" %}

.. code:: text

    [myapp]
    log_handler = logging

    [log.logging]
    to_console = true
    file = /path/to/myapp.log
    level = warning

{% endtab %}

{% tab title="cli" %}

.. code:: text

    $ python myapp.py
    INFO: this is an info message
    WARNING: this is an warning message
    ERROR: this is an error message
    CRITICAL: this is an fatal message

{% endtab %} {% endtabs %}

Output
------

By default, Cement does not define any output handlers. Just like any
other app, you are free to ``print()`` to console all you like or use
the builtin logging facility. That said, more complex applications will
benefit greatly by separating the output from the logic. Think of output
handling as the ``view`` in a traditional `MVC
Framework <https://en.wikipedia.org/wiki/Model-view-controller>`__.

Cement ships with several types of extensions that produce output in
different forms, including the following:

-  Text Rendered From Template Files
-  Programatic Structures (JSON, Yaml, etc)
-  Tabulated (like MySQL, etc)
-  Etc

The following output handlers ship with Cement:

-  `Json <../extensions/json.md>`__ - Produces JSON output from dicts
-  `Yaml <../extensions/yaml.md>`__ - Produces Yaml output from dicts
-  `Mustache <../extensions/mustache.md>`__ - Produces text output
   rendered from `Mustache <http://mustache.github.io/>`__ templates
-  `Handlebars <framework-overview.md>`__ - Produces text output
   rendered from `Handlebars <https://github.com/wbond/pybars3>`__
   templates
-  `Jinja2 <../extensions/jinja2.md>`__ - Produces text output rendered
   from `Jinja2 <http://jinja.pocoo.org/>`__ templates
-  `Tabulated <../extensions/tabulate.md>`__ - Produces tabulated text
   output rendered via the
   `Tabulate <https://pypi.python.org/pypi/tabulate>`__ library.

**Multiple Output Handler Support**

One of the unique features of Cement is that you can build your
application to support multiple output handlers and formats. Output
handlers have a special attribute that *optionally* allows them to be
exposed via the CLI option ``-o`` (configurable via
```Handler.Meta.overridable`` <http://cement.readthedocs.io/en/3.0/api/core/handler/#cement.core.handler.Handler.Meta.overridable>`__
and
```App.Meta.core_handler_override_options`` <https://cement.readthedocs.io/en/portland/api/core/foundation/#cement.core.foundation.App.Meta.core_handler_override_options>`__).
Therefore, you might have default text based output rendered from
Mustache templates, but optionally output programatic structures **from
the same code** when necessary (i.e.``$ myapp -o json``).

Ex: Mixed Template/JSON Output Example

{% tabs %} {% tab title="myapp.py" %}

.. code:: python

    from cement import App, init_defaults

    META = init_defaults('output.json')
    META['output.json']['overridable'] = True

    class MyApp(App):
        class Meta:
            label = 'myapp'

            ### override default handler meta options
            meta_defaults = META

            ### add optional extensions
            extensions = ['json', 'mustache']

            ### set the default output handler
            output_handler = 'mustache'

            ### external template directory
            template_dir = '/path/to/templates'

            ### internal template module (shipped with app code)
            template_module = 'myapp.templates'


    with MyApp() as app:
        app.run()

        ### create some data
        data = {
            'foo' : 'bar',
        }

        ### render data using mustache template (by default)
        app.render(data, 'example.m')

{% endtab %}

{% tab title="templates/example.m" %}

.. code:: text

    The value of foo={{foo}}.

{% endtab %}

{% tab title="cli" %}

.. code:: text

    $ python myapp.py --help
    usage: myapp [-h] [--debug] [--quiet] [-o {json}]

    optional arguments:
      -h, --help  show this help message and exit
      --debug     toggle debug output
      --quiet     suppress all output
      -o {json}   output handler


    $ python myapp.py
    The value of foo=bar


    $ python myapp.py -o json
    {"foo": "bar"}

{% endtab %} {% endtabs %}

Controllers
-----------

Controllers provide a common means of organizing application logic into
relevant chunks of code, as well as the ability for plugins and
extensions to extend an applications capabilities. It is the
``Controller`` piece of the traditional `MVC
Framework <https://en.wikipedia.org/wiki/Model-view-controller>`__.

The first controller is called ``base``, and if registered will take
over runtime control when ``app.run()`` is called. What this means is,
instead of Cement calling ``app.args.parse_arguments()`` directly, the
`runtime dispatch <../terminology.md#runtime-dispatch>`__ is handed over
to the ``base`` controller, that is then responsible for parsing and
handling arguments.

The most notable action of runtime dispatch is mapping arguments and
sub-commands to their respective controllers and functions. For example,
the default action when running ``$ myapp`` without any arguments or
sub-commands is to execute the ``Base._default()`` function.

Ex: Application Base Controller

{% tabs %} {% tab title="myapp.py" %}

.. code:: python

    from cement import App, Controller, ex


    class Base(Controller):
        class Meta:
            label = 'base'

            arguments = [
                # list of tuples in the format `( [], {} )`
                ( [ '-a' ],
                  { 'help' : 'example a option',
                    'dest' : 'a' } ),
            ]

        def _default(self):
            print('Inside Base._default()')
            if self.app.pargs.a:
                print('Received Option: -a')

        @ex(
            help='sub-command under base controller',
            arguments=[
                ( [ '-b' ],
                  { 'help' : 'cmd1 b option' } ),
            ]
        )
        def cmd1(self):
            print('Inside Base.cmd1()')
            if self.app.pargs.b:
                print('Recieved Option: -b')


    class MyApp(App):
        class Meta:
            label = 'myapp'
            handlers = [
                Base,
            ]


    with MyApp() as app:
        app.run()

{% endtab %}

{% tab title="cli" %}

.. code:: text

    ### help output shows base namespace arguments and sub-commands

    $ python myapp.py --help
    usage: myapp [-h] [--debug] [--quiet] [-a A] {cmd1} ...

    optional arguments:
      -h, --help  show this help message and exit
      --debug     toggle debug output
      --quiet     suppress all output
      -a A        example a option

    sub-commands:
      {cmd1}
        cmd1      sub-command under base controller


    $ python myapp.py -a foo
    Inside Base._default()
    Received Option: -a


    ### sub-commands support their own arguments

    $ python myapp.py cmd1 --help
    usage: myapp cmd1 [-h] [-b B]

    optional arguments:
      -h, --help  show this help message and exit
      -b B        cmd1 b option


    $ python myapp.py cmd1 -b foo
    Inside Base.cmd1()
    Recieved Option: -b

{% endtab %} {% endtabs %}

**Nested / Embedded Controllers**

Cement supports two types of `controller
stacking <../terminology.md#controller-stacking>`__:

-  **nested** - The arguments and commands are nested under a sub-parser
   whose label is that of the controller. For example, a nested
   controller with a label of ``my-nested-controller`` would be called
   as ``$ myapp my-nested-controller sub-command``.
-  **embedded** - The arguments and commands are embedded within it's
   parent controller, therefore appearing as if they were defined by the
   parent itself. A sub-command under an embedded controller would be
   called as ``$ myapp sub-command``.

Controllers can be stacked on other controllers as many levels deep as
necessary. An ``embedded`` controller can be stacked on top of a
``nested`` controller, and vice versa. There is little, if any,
limitation.

**Controller Arguments vs Command Arguments**

Both Controllers and their sub-commands can have arguments defined.
Think of controllers as the primary namespace. It's arguments should be
globally relevant within that namespace. A sub-command within the
namespace can have it's own arguments, but are only relevant to that
sub-command.

Ex: ``$ myapp -a my-controller -b my-sub-command -c``

In the above example, ``-a`` is relevant to the global scope of the
entire application because it is defined on the ``base`` controller.
Option ``-b`` is relevant to the scope of ``my-controller`` and all
sub-commands under it. Finally, ``-c`` is only relevant to the
``my-sub-command`` and has no use elsewhere.

**Exposing Sub-Commands**

By default, no commands are exposed to the CLI except that a
``_default()`` function will be called if no sub-command is passed
(configurable by ``Controller.Meta.default_func``).

To expose a function as a sub-command, you must decorate it with
``@ex()``. It's usage is simple, and supports the following parameters:

-  ``hide`` (*bool*) - Whether or not to display in ``--help`` output.
-  ``arguments`` (*list*) - Argument list of tuples in the format
   ``( [], {} )``, that are passed to
   ``Argparse.add_argument(*args, **kwargs)``.
-  ``**kwargs`` - Additional keyword arguments are passed directly to
   Argparse when creating the sub-parser for this command.

{% hint style="info" %} The term ``ex`` is short for ``expose``, and
allows for shorter reference and also four character
indentation/alignment with functions to be easier on the eyes. {%
endhint %}

Framework Extensions
--------------------

Cement's `Interfaces and
Handlers <../core-foundation/interfaces-and-handlers.md>`__ system makes
extending the framework easy, and limitless. Cement ships with dozens of
extensions that either alter existing functionality, or add to it. For
example, the default logging facility provides basic logging
capabilities, however with a single line of code an application can
instead use the `Colorlog <../extensions/colorlog.md>`__ extension to
enable colorized console logging.

The following example provides a quick look at using the
`Alarm <../extensions/alarm.md>`__ extension to handle application
timeouts of long running operations

Ex: Using Framework Extensions:

{% tabs %} {% tab title="myapp.py" %}

.. code:: python

    from time import sleep
    from cement import App


    class MyApp(App):
        class Meta:
            label = 'myapp'
            extensions = ['alarm']


    with MyApp() as app:
        app.run()

        ### set an alarm for max allowed run time
        app.alarm.set(3, "The operation timed out after 3 seconds!")

        ### do something that takes time to operate
        sleep(5)

        ### stop the alarm if it ran within the time frame
        app.alarm.stop()

{% endtab %}

{% tab title="cli" %}

.. code:: text

    $ python myapp.py
    ERROR: The operation timed out after 3 seconds!
    Traceback (most recent call last):
      File "myapp.py", line 20, in <module>
        sleep(5)
      File "cement/core/foundation.py", line 123, in cement_signal_handler
        raise exc.CaughtSignal(signum, frame)
    cement.core.exc.CaughtSignal: Caught signal 14

{% endtab %} {% endtabs %}

See the `Extensions
Documentation <../core-foundation/extensions-1.md>`__ to learn more
about the extended capabilities of the framework.

Application Plugins
-------------------

Cement provides an interface that automatically handles the management,
configuration, and loading of Application Plugins. A Plugin is
essentially the same as a Framework Extension, but is application
specific where extensions are agnostic (can be used by any application).

A plugin can be anything, and provide any kind of functionality from
defining runtime hooks, to extending an applications capabilities by
adding nested/embedded controllers. The only thing that a plugin must
provide is a ``load()`` function that is called when the plugin is
imported.

Ex: Basic Application

{% tabs %} {% tab title="myapp.py" %}

.. code:: python

    from cement import App, Controller, ex


    class Base(Controller):
        class Meta:
            label = 'base'


    class MyApp(App):
        class Meta:
            label = 'myapp'
            handlers = [
                Base,
            ]


    with MyApp() as app:
        app.run()

{% endtab %}

{% tab title="cli" %}

.. code:: text

    $ python test.py --help
    usage: myapp [-h] [--debug] [--quiet] {} ...

    optional arguments:
      -h, --help  show this help message and exit
      --debug     toggle debug output
      --quiet     suppress all output

    sub-commands:
      {}

{% endtab %} {% endtabs %}

Using the same application, we can create a plugin to extend
functionality:

Ex: Application Plugin

{% tabs %} {% tab title="myplugin.py" %}

.. code:: python

    from cement import Controller, ex


    class MyPlugin(Controller):
        class Meta:
            label = 'myplugin'
            stacked_on = 'base'
            stacked_type = 'embedded'

        @ex()
        def cmd1(self):
            print('Inside MyPlugin.cmd1()')


    def load(app):
        app.handler.register(MyPlugin)

{% endtab %}

{% tab title="~/.myapp.conf" %}

.. code:: text

    [myapp]
    plugin_dir = /path/to/myapp/plugins

    [plugin.myplugin]
    enabled = true

{% endtab %}

{% tab title="cli " %}

.. code:: text

    $ python myapp.py --help
    usage: myapp [-h] [--debug] [--quiet] {cmd1} ...

    optional arguments:
      -h, --help  show this help message and exit
      --debug     toggle debug output
      --quiet     suppress all output

    sub-commands:
      {cmd1}


    $ python myapp.py cmd1
    Inside MyPlugin.cmd1()

{% endtab %} {% endtabs %}

Hooks
-----

Hooks provide developers the ability to tie into the framework, and
applications without direct access to the runtime. For example, a plugin
might need to execute some code after arguments have been parsed, but
before controller sub-commands are dispatched. As a plugin developer,
you don't have direct access to the applications runtime code but you
can still tie into it with the builtin ``post_argument_parsing`` hook.

Cement defines several hooks that tie in to specific points throughout
the application life cycle, however application developers can also
define their own hooks allowing others to tie elsewhere, when needed.

Ex: Executing Code Via Hooks

{% tabs %} {% tab title="myapp.py" %}

.. code:: python

    from cement import App


    def my_example_hook(app):
        print('Inside my_example_hook()')


    class MyApp(App):
        class Meta:
            label = 'myapp'
            hooks = [
                ('post_argument_parsing', my_example_hook),
            ]


    with MyApp() as app:
        app.run()

{% endtab %}

{% tab title="cli" %}

.. code:: text

    $ python myapp.py
    Inside my_example_hook()

{% endtab %} {% endtabs %}
