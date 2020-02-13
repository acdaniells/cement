# Logging

## Introduction

The Logging Extension includes the LoggingLogHandler, and provides log handling based on the standard [`logging`](https://docs.python.org/3.6/library/logging.html#logging.Logger) library.

**Documentation References:**

* [Logging](../core-foundation/logging-1.md)

**API References:**

* [Cement Logging Extension](https://cement.readthedocs.io/en/3.0/api/ext/ext_logging/)
* [Python Logging Library](https://docs.python.org/3/library/logging.html)

## Requirements

* No external dependencies

## Configuration

### Application Configuration Settings

This handler honors the following settings under a `[log.logging]` section of the configuration:

| **Setting** | **Description** |
| :--- | :--- |
| **level** | The logging to display logs for. One of `INFO, WARNING, ERROR, FATAL, DEBUG`. Default: `INFO` |
| **file** | The filesystem path of the log file.  Default: `None` |
| **to\_console** | Whether or not to log to console.  Default: `True` |
| **rotate** | Whether or not rotate the log file.  Default: `False` |
| **max\_bytes** | Maximum file size \(in bytes\) until the log file is rotated \(if rotation is enabled\).  Default: _512000_ |
| **max\_files** | Maximum number of files to keep when rotating is enabled.  Default: `4` |

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
```
{% endcode-tabs-item %}
{% endcode-tabs %}

### **Toggle Log Level via Command-line**

This extension supports an optional feature to add a command-line argument to toggle the log level. This feature is not enabled by default for one specific reason: the log level will not be modified until **after** argument parsing happens. This can lead to a lot of confusion for developers who might not see their debug logs from a `pre_setup` hook, or anything that happens before argument parsing completes. For this reason, you should use this feature with caution and thus we disable it by default.

You can enable the log level argument by setting via [`App.Meta.meta_defaults`](https://cement.readthedocs.io/en/3.0/api/core/foundation/#cement.core.foundation.App.Meta.meta_defaults) for the `log.logging` handler:

{% tabs %}
{% tab title="Example: Enabling Log Level Argument" %}
```python
from cement import App, init_defaults

META = init_defaults('log.logging')
META['log.logging']['log_level_argument'] = ['-l', '--level']

class MyApp(App):
    class Meta:
        label = 'myapp'
        meta_defaults = META
```
{% endtab %}

{% tab title="cli" %}
```text
$ python myapp.py --help
usage: myapp [-h] [--debug] [--quiet] [-l {info,warning,error,debug,fatal}]

optional arguments:
  -h, --help            show this help message and exit
  --debug               full application debug mode
  --quiet               suppress all output
  -l {info,warning,error,debug,fatal}
                        logging level


$ python myapp.py
INFO: This is an info message
WARNING: This is an warning message
ERROR: This is an error message
CRITICAL: This is a fatal message

$ python myapp.py -l error
ERROR: This is an error message
CRITICAL: This is a fatal message
```
{% endtab %}
{% endtabs %}

## Usage

See the [Logging Documentation](../core-foundation/logging-1.md).

