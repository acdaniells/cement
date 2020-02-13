# Configuration Settings

## Introduction to the Config Interface

Cement defines a [Config Interface](http://cement.readthedocs.io/en/3.0/api/core/config/#cement.core.config.ConfigInterface), as well as the default [ConfigParserConfigHandler](http://cement.readthedocs.io/en/3.0/api/ext/ext_configparser/#cement.ext.ext_configparser.ConfigParserConfigHandler) that implements the interface. This handler is built on top of [ConfigParser](http://docs.python.org/library/configparser.html) which is included in the Python standard library. Therefore, this class will work much like ConfigParser but with any added functions necessary to meet the requirements of the interface.

{% hint style="warning" %}
Cement often includes multiple handler implementations of an interface that may or may not have additional features or functionality than the interface requires. The documentation below only references usage based on the interface and default handler \(not the full capabilities of an implementation\).
{% endhint %}

**Cement Extensions That Provide Config Handlers:**

* [ConfigParser](../extensions/configparser.md) _\(default\)_
* [Json](../extensions/json.md)
* [Yaml](../extensions/yaml.md)

**API References:**

* [Cement Core Config Module](https://cement.readthedocs.io/en/3.0/api/core/config/)
* [Cement ConfigParser Extension](https://cement.readthedocs.io/en/3.0/api/ext/ext_configparser/)
* [Python ConfigParser Library](https://docs.python.org/3/library/configparser.html)

## **Configuration**

### **Application Meta Options**

The following options under [`App.Meta`](https://cement.readthedocs.io/en/3.0/api/core/foundation/#cement.core.foundation.App.Meta) modify configuration handling:

| **Option** | **Description** |
| :--- | :--- |
| **config\_defaults** | Default configuration dictionary. |
| **config\_dirs** | List of configuration directory paths where config files will be loaded from.  These are merged together with `App.Meta.core_system_config_dirs` and `App.Meta.core_user_config_dirs` |
| **config\_file\_suffix** | The suffix \(extension\) of configuration files.  Default: `.conf` |
| **config\_files** | List of configuration file paths to load. |
| **config\_handler** | The configuration handler that implements the config interface. |
| **config\_section** | The section label of the application's configuration within config files. Defaults: `App.Meta.label` |

## Configuration Load Order

An application's configuration is made up of a number of things, including default settings, handler defaults, config file settings, environment variables, etc. The following is the order in which configurations are discovered and loaded:

* Defaults defined in [`App.Meta.config_defaults`](http://cement.readthedocs.io/en/3.0/api/core/foundation/#cement.core.foundation.App.Meta.config_defaults)
* Extended by [`Handler.Meta.config_defaults`](http://cement.readthedocs.io/en/3.0/api/core/handler/#cement.core.handler.Handler.Meta.config_defaults) _\(extended, not overridden\)_
* Overridden by configuration files defined in [`App.Meta.config_files`](http://cement.readthedocs.io/en/3.0/api/core/foundation/#cement.core.foundation.App.Meta.config_files) in the order they are listed/loaded \(last has precedence\)
* Overridden by environment variables \(ex: `$MAPP_FOO` `$MYAPP_LOG_LOGGING_LEVEL`, etc\)

## Application Default Settings

Cement does not require default config settings in order to operate. That said, these settings are found under the `App.Meta.label` section of the configuration, and overridden by a `[<app_label>]` block from configuration files.

{% tabs %}
{% tab title="Example: Setting Application Defaults" %}
{% code-tabs %}
{% code-tabs-item title="myapp.py" %}
```python
from cement import App, init_defaults


CONFIG = init_defaults('myapp', 'log.logging')
CONFIG['myapp']['foo'] = 'bar'
CONFIG['log.logging']['level'] = 'info'

class MyApp(App):
    class Meta:
        label = 'myapp'
        config_defaults = CONFIG
```
{% endcode-tabs-item %}

{% code-tabs-item title="~/.myapp.conf" %}
```text
[myapp]
foo = bar

[log.logging]
level = info
```
{% endcode-tabs-item %}
{% endcode-tabs %}
{% endtab %}
{% endtabs %}

{% hint style="info" %}
Note that `init_defaults` is a helper from the Miscellaneous Utility Module, and simply generates a dict with nested dicts of the given keys. It does not do anything special, but is used throughout the documentation as it generally makes things more readable in examples.

You can always use a standard `dict` for configuration and meta defaults, which often makes more sense when building larger applications with a lot of default settings to manage.
{% endhint %}

## Builtin Default Configuration Settings

Cement defines a list of meta options that can be overridden by configuration settings in [`App.Meta.core_meta_override`](http://cement.readthedocs.io/en/3.0/api/core/foundation/#cement.core.foundation.App.Meta.core_meta_override) \(used by the framework\), and [`App.Meta.meta_override`](http://cement.readthedocs.io/en/3.0/api/core/foundation/#cement.core.foundation.App.Meta.meta_override) \(used by the application developer\). These are not required to exist in the config defaults or parsed configuration files. However, if they do, Cement will honor them and override the defined application meta options.

## Configuration File Loading

Cement defines the following builtin default configuration file paths:

```text
/etc/myapp/myapp.conf
~/.config/myapp/myapp.conf
~/.myapp/config/myapp.conf
~/.myapp.conf
```

We also define the following configuration directories to scan for additional configuration files for extensions and plugins:

```text
/etc/myapp/ext.d
/etc/myapp/plugins.d
~/.config/myapp/ext.d
~/.config/myapp/plugins.d
~/.myapp/config/ext.d
~/.myapp/config/plugins.d
```

{% hint style="info" %}
These lists are dynamically generated based on the `App.meta.label`, as well as [`App.meta.config_file_suffix`](https://cement.readthedocs.io/en/3.0/api/core/foundation/#cement.core.foundation.App.Meta.config_file_suffix). They can be extended by adding files via [`App.Meta.config_files`](https://cement.readthedocs.io/en/3.0/api/core/foundation/#cement.core.foundation.App.Meta.config_files) or directories to [`App.Meta.config_dirs`](https://cement.readthedocs.io/en/3.0/api/core/foundation/#cement.core.foundation.App.Meta.config_dirs).
{% endhint %}

## Accessing Configuration Settings

After application creation and setup, you can access the config handler via the `app.config` object.

{% tabs %}
{% tab title="Example: Using App Config Object" %}
```python
from cement import App

with App('myapp') as app:
    app.run()

    ​# get a setting
    app.config.get('myapp', 'debug')

    ​# set settings
    app.config.set('myapp', 'debug', True)

    ​# get a list of sections
    app.config.get_sections()​

    # add a section
    app.config.add_section('my_config_section')

    ​# test if a section exists
    app.config.has_section('my_config_section')​

    # get configuration keys for the 'myapp' section
    app.config.keys('myapp')​

    # test if a key exists
    if 'debug' in app.config.keys('myapp')​:
        pass

    # merge a dict of settings into the config
    other_config = {
        'myapp': {
            'foo': 'not bar',
        }
    }
    app.config.merge(other_config)

    # parse a file into the config
    app.config.parse('/path/to/file')

    # get a dict of the entire config
    app.config.get_dict()
```
{% endtab %}
{% endtabs %}

## Configuration Settings vs. Meta Options

As you will see extensively throughout the Cement code is the use of meta options. There can be some confusion between the use of meta options, and application configuration settings.

{% hint style="info" %}
The key detail to note is that configuration settings are intended to be used and modified by the **end-user**, whereas meta options are intended to be used by the application **developer** to alter the application's core functionality.
{% endhint %}

**Configuration Settings**

Configuration settings are application specific. There are config defaults defined by the application developer, that can be \(and are intended to be\) overridden by end-user defined settings in a configuration file.

Cement does not rely on the application configuration, though it can honor configuration settings. For example, `App` honors the `debug` config option which is documented, but it doesn't rely on it existing either.

The key things to note about application configuration settings are:

* They give the **end-user** flexibility in how the application operates.
* Anything that you want users to be able to customize via a config file should be defined in the application's configuration. For example, the path to a log file or the location of a database server. These are things that you do not want hard-coded into your app, but rather should have sane and functional defaults for.

**Meta Options**

Meta options are used on the backend by developers to alter how classes operate. For example, the [`App.Meta.log_handler`](http://cement.readthedocs.io/en/3.0/api/core/foundation/#cement.core.foundation.App.Meta.log_handler) defines the default log handler as `logging` \(`cement.ext.ext_logging.LoggingLogHandler`\), however because this is built on an interface definition, Cement can use any other log handler the same way without issue as long as that log handler properly implements the interface definition. Meta options make this change seamless and allows the handler to alter functionality, rather than having to change code in the top level class itself.

The key thing to note about meta options are:

* They give the **developer** flexibility in how the code operates.
* End users should not have access to modify meta options via a config file or similar 'dynamic' configuration unless explicitly listed in [`Cement.Meta.core_meta_override`](http://cement.readthedocs.io/en/3.0/api/core/foundation/#cement.core.foundation.App.Meta.core_meta_override) or [`CementApp.Meta.meta_override`](http://cement.readthedocs.io/en/3.0/api/core/foundation/#cement.core.foundation.App.Meta.meta_override) \(for example, the `debug` setting under the `[<app_label>]` section overrides `App.Meta.debug` by default.
* Meta options are used to alter how classes work, but they are considered 'hard-coded' settings. If the developer chooses to alter a meta option, it is for the life of that release.
* Meta options should have a sane default, and be clearly documented.

## Application Defaults vs Handler Defaults

There may be slight confusion between the [`App.Meta.config_defaults`](http://cement.readthedocs.io/en/3.0/api/core/foundation/#cement.core.foundation.App.Meta.config_defaults) and the [`Handler.Meta.config_defaults`](http://cement.readthedocs.io/en/3.0/api/core/handler/#cement.core.handler.Handler.Meta.config_defaults) meta options. They both are very similar, however the application level configuration defaults are intended to be used to set defaults for multiple sections. Therefore, the `App.Meta.config_defaults` option is a `dict` with nested `dict`s under it. Each key of the top level `dict` relates to a config `[section]` and the nested `dict`s are the settings for that `[section]`.

The `Handler.Meta.config_defaults` only pertain to a single `[section]` and therefore is only a single level `dict`, whose settings are applied to that section of the application's configuration \(defined by [`Handler.Meta.config_section`](http://cement.readthedocs.io/en/3.0/api/core/handler/#cement.core.handler.Handler.Meta.config_section)\).

## Creating a Config Handler

All interfaces in Cement can be overridden with your own implementation. This can be done either by sub-classing [`ConfigHandler`](https://cement.readthedocs.io/en/3.0/api/core/config/#cement.core.config.ConfigHandler) itself, or by sub-classing an existing extension's handlers in order to alter their functionality.

{% tabs %}
{% tab title="Example: Creating a Config Handler" %}
{% code-tabs %}
{% code-tabs-item title="myapp.py" %}
```python
from cement import App
from cement.core.config import ConfigHandler

class MyConfigHandler(ConfigHandler):
    class Meta:
        label = 'my_config_handler'

    # do something to implement the interface

class MyApp(App):
    class Meta:
        label = 'myapp'
        config_handler = 'my_config_handler'
        handlers = [
            MyConfigHandler,
        ]
```
{% endcode-tabs-item %}
{% endcode-tabs %}
{% endtab %}
{% endtabs %}

