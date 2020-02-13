# Logging

## Introduction to the Log Interface

Cement defines the [Log Interface](https://cement.readthedocs.io/en/3.0/api/core/log/#cement.core.log.LogInterface), as well as the default [LoggingLogHandler](https://cement.readthedocs.io/en/3.0/api/ext/ext_logging/#cement.ext.ext_logging.LoggingLogHandler) that implements the interface. This handler is built on top of the [Logging](http://docs.python.org/library/logging.html) module which is included in the Python standard library.

{% hint style="warning" %}
Cement often includes multiple handler implementations of an interface that may or may not have additional features or functionality than the interface requires. The documentation below only references usage based on the interface and default handler \(not the full capabilities of an implementation\).
{% endhint %}

**Cement Extensions That Provide Log Handlers**

* [Logging](../extensions/logging.md)
* [Colorlog](../extensions/colorlog.md)

**API References:**

* [Cement Core Log Module](https://cement.readthedocs.io/en/3.0/api/core/log/)
* [Cement Logging Extension](https://cement.readthedocs.io/en/3.0/api/ext/ext_logging/)

## **Configuration**

### **Application Meta Options**

The following options under [`App.Meta`](https://cement.readthedocs.io/en/3.0/api/core/foundation/#cement.core.foundation.App.Meta) modify configuration handling:

| **Option** | **Description** |
| :--- | :--- |
| **log\_handler** | The handler that implements the log interface. |

## Logging Messages

The following shows logging to each of the defined log levels.

{% tabs %}
{% tab title="Example: Log Levels" %}
```python
from cement import App

with App('myapp') as app:
    app.run()

    ​# log messages to different levels
    app.log.debug('This is a debug message.')
    app.log.info('This is an info message.')​
    app.log.warning('This is a warning message.')
    app.log.error('This is an error message.')
    app.log.fatal('This is a fatal message.')​
```
{% endtab %}
{% endtabs %}

The above is displayed in order of severity. If the log level is set to `INFO`, you will receive all info messages and above including `WARNING`, `ERROR`, and `FATAL`. However, you will not receive `DEBUG` level messages. The same goes for a log level of `WARNING`, where you will receive `WARNING`, `ERROR`, and `FATAL` but you will not receive INFO, or `DEBUG` level messages.

## Changing Log Level

The log level defaults to `INFO`, but can be set via [`LoggingLogHandler.Meta.config_defaults`](https://cement.readthedocs.io/en/3.0/api/ext/ext_logging/#cement.ext.ext_logging.LoggingLogHandler.Meta.config_defaults) or setting the `level` under the log handlers section of the application configuration:

{% tabs %}
{% tab title="Example: Changing Log Level" %}
{% code-tabs %}
{% code-tabs-item title="myapp.py" %}
```python
from cement import App, init_defaults

CONFIG = init_defaults('myapp', 'log.logging')
CONFIG['log.logging']['level'] = 'WARNING'

class MyApp(App):
    class Meta:
        label = 'myapp'
        config_defaults = CONFIG
```
{% endcode-tabs-item %}

{% code-tabs-item title="~/.myapp.conf" %}
```text
[myapp]

# ...

[log.logging]
level = WARNING
```
{% endcode-tabs-item %}
{% endcode-tabs %}
{% endtab %}
{% endtabs %}

{% hint style="info" %}
Cement also includes a `--debug` command line option by default. This triggers `App.Meta.debug` and sets the log level to `DEBUG`.
{% endhint %}

## Logging to Console

The default log handler configuration enables logging messages to console.

{% tabs %}
{% tab title="Example: Logging to Console" %}
```python
from cement import App

with App('myapp') as app:
    app.run()

    # log messages to different levels
    app.log.debug('This is a debug message')
    app.log.info('This is an info message')
    app.log.warning('This is an warning message')
    app.log.error('This is an error message')
    app.log.fatal('This is a fatal message')
```
{% endtab %}

{% tab title="cli" %}
```text
$ python myapp.py
INFO: This is an info message
WARNING: This is a warning message
ERROR: This is an error message
CRITICAL: This is a fatal message
```
{% endtab %}
{% endtabs %}

{% hint style="info" %}
Console logging can be disabled by setting `to_console` to `False` in either the application defaults, or under the `[log.logging]` section of the applications configuration file.
{% endhint %}

## Logging to File

File logging is disabled by default but can be enabled by setting the `file` setting under the `[log.logging]` section of the application configuration.

{% tabs %}
{% tab title="Example: Logging to File" %}
{% code-tabs %}
{% code-tabs-item title="myapp.py" %}
```python
from cement import App, init_defaults

CONFIG = init_defaults('myapp', 'log.logging')
CONFIG['log.logging']['file'] = '/path/to/file.log'

class MyApp(App):
    class Meta:
        label = 'myapp'
        config_defaults = CONFIG
```
{% endcode-tabs-item %}

{% code-tabs-item title="~/.myapp.conf" %}
```text
[myapp]
# ...

[log.logging]
file = /path/to/file.log
```
{% endcode-tabs-item %}
{% endcode-tabs %}
{% endtab %}
{% endtabs %}

## Tips on Debugging

{% hint style="info" %}
The following is specific to the default [`LoggingLogHandler`](https://cement.readthedocs.io/en/3.0/api/ext/ext_logging/#cement.ext.ext_logging.LoggingLogHandler), and is not an requirement of the logging interface.
{% endhint %}

Logging to `app.log.debug()` is pretty straightforward. However, adding an additional parameter for the `namespace` can greatly increase insight into where that log is happening. The `namespace` defaults to the application name which you will see in every log like this:

```text
2012-07-30 18:05:11,357 (DEBUG) myapp : This is my message
```

For debugging, it might be more useful to change this to `__name__`:

```python
app.log.debug('This is my info message', __name__)
```

Which looks like:

```text
2012-07-30 18:05:11,357 (DEBUG) myapp.somepackage.test : This is my message
```

Or even more verbose, you might prefer adding something like `__file__` and the function or class method:

```python
app.log.debug('This is my info message', '%s : my_func()' % __file__)
```

Which would look like:

```text
2012-07-30 18:05:11,357 (DEBUG) myapp/somepackage/test.py : my_func() : This is my message
```

## Creating a Log Handler

All interfaces in Cement can be overridden with your own implementation. This can be done either by sub-classing [`LogHandler`](https://cement.readthedocs.io/en/3.0/api/core/log/#cement.core.log.LogHandler) itself, or by sub-classing an existing extension's handlers in order to alter their functionality.

{% tabs %}
{% tab title="Example: Creating a Log Handler" %}
{% code-tabs %}
{% code-tabs-item title="myapp.py" %}
```python
from cement import App
from cement.core.log import LogHandler

class MyLogHandler(LogHandler):
    class Meta:
        label = 'my_log_handler'

    # do something to implement the interface

class MyApp(App):
    class Meta:
        label = 'myapp'
        log_handler = 'my_log_handler'
        handlers = [
            MyLogHandler,
        ]
```
{% endcode-tabs-item %}
{% endcode-tabs %}
{% endtab %}
{% endtabs %}

