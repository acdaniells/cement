# Colorlog

## Introduction

The ColorLog Extension provides the [`ColorLogHandler`](http://cement.readthedocs.io/en/3.0/api/ext/ext_colorlog/#cement.ext.ext_colorlog.ColorLogHandler) for logging, and is a sub-class and drop-in replacement for the default log handler [`LoggingLogHandler`](http://cement.readthedocs.io/en/3.0/api/ext/ext_logging/#cement.ext.ext_logging.LoggingLogHandler).

**Documentation References:**

* [Logging](../core-foundation/logging-1.md)

**API References:**

* [Cement Colorlog Extension](http://cement.readthedocs.io/en/3.0/api/ext/ext_colorlog/)
* [Colorlog Module](https://pypi.org/project/colorlog/)

## Requirements

* Colorlog \(`pip install colorlog)`

## Configuration

This handler honors the following settings under a `[log.colorlog]` section of the configuration:

| **Setting** | **Description** |
| :--- | :--- |
| **level** | The level to display logs for.  One of `INFO`, `WARNING`, `ERROR`, `FATAL`, `DEBUG`.  Default: `INFO` |
| **file** | The filesystem path of the log file.  Default: `None` |
| **to\_console** | Whether or not to log to console.  Default: `True` |
| **rotate** | Whether or not rotate the log file.  Default: `False` |
| **max\_bytes** | Maximum file size \(in bytes\) until the log file is rotated \(if rotation is enabled\).  Default: _512000_ |
| **max\_files** | Maximum number of files to keep when rotating is enabled.  Default: `4` |
| **colorize\_file\_log** | Whether or not to colorize the log file.  Default: `False` |
| **colorize\_console\_log** | Whether or not to colorize the console log.  Default: `True` |

{% hint style="warning" %}
Note that there are precautions in place to disable colorized logging if the session is not a valid TTY via `sys.stdout.istty()`
{% endhint %}

A sample config section might look like:

{% code-tabs %}
{% code-tabs-item title="~/.myapp.conf" %}
```text
[log.colorlog]
file = /path/to/config/file
level = info
to_console = true
rotate = true
max_bytes = 512000
max_files = 4
colorize_file_log = false
colorize_console_log = true
```
{% endcode-tabs-item %}
{% endcode-tabs %}

## Usage

{% tabs %}
{% tab title="Example: Using Colorlog Extension" %}
```python
from cement import App

class MyApp(App):
    class Meta:
        label = 'myapp'
        extensions = ['colorlog']
        log_handler = 'colorlog'

with MyApp() as app:
    app.run()
    app.log.debug('This is my debug message')
    app.log.info('This is my info message')
    app.log.warning('This is my warning message')
    app.log.error('This is my error message')
    app.log.fatal('This is my critical message')
```
{% endtab %}
{% endtabs %}

{% hint style="info" %}
The colors can be customized by passing in a `colors` dictionary mapping overriding the [`ColorLogHandler.Meta.colors`](http://cement.readthedocs.io/en/3.0/api/ext/ext_colorlog/#cement.ext.ext_colorlog.ColorLogHandler.Meta.colors) option
{% endhint %}

{% tabs %}
{% tab title="Example: Customizing Colorlog Colors" %}
```python
from cement import App, init_defaults

META = init_defaults('log.colorlog')
META['log.colorlog']['colors'] = {
    'DEBUG':    'cyan',
    'INFO':     'green',
    'WARNING':  'yellow',
    'ERROR':    'red',
    'CRITICAL': 'red,bg_white',
}

class MyApp(App):
    class Meta:
        label = 'myapp'
        extension = ['colorlog']
        log_handler = 'colorlog'
        meta_defaults = META
```
{% endtab %}
{% endtabs %}

