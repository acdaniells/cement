# Application Plugins

## Introduction to the Plugin Interface

Cement defines a Plugin Interface, as well as the default [CementPluginHandler](https://cement.readthedocs.io/en/3.0/api/ext/ext_plugin/#cement.ext.ext_plugin.CementPluginHandler) that implements the interface.

{% hint style="warning" %}
Cement often includes multiple handler implementations of an interface that may or may not have additional features or functionality than the interface requires. The documentation below only references usage based on the interface and default handler \(not the full capabilities of an implementation\).
{% endhint %}

**Cement Extensions that Provide Plugin Handlers:**

* [Plugin](../extensions/plugin.md)

**API References:**

* [Cement Core Plugin Module](https://cement.readthedocs.io/en/3.0/api/core/plugin/)

## Configuration

### Application Configuration Settings

The following settings under the application's primary configuration section modify plugin handling:

| **Setting** | **Description** |
| :--- | :--- |
| **plugin\_dir** | A directory path where plugin code can be found.  Will be **prepended** to `App.Meta.plugin_dirs` |

### Application Meta Options:

The following options under [`App.Meta`](https://cement.readthedocs.io/en/3.0/api/core/foundation/#cement.core.foundation.App.Meta) modify plugin handling:

| **Option** | **Description** |
| :--- | :--- |
| **plugins** | A _hardcoded_ list of plugins to load.  In general, application plugins should be dynamically enabled/disabled via the application's configuration files.  However, some application designs may prefer to always load specific builtin plugins. Default: `[]` |
| **config\_dirs** | Plugin configuration files are loaded from any discovered application configuration directories. |
| **plugin\_module** | A python module \(dotted import path\) where plugin code can be loaded from instead of external directories \(builtin plugins shipped with the application code\).  Default: `myapp.plugins` |
| **plugin\_dirs** | A list of directory paths where plugin code \(modules\) can be loaded from \(external to the application\).  Will be merged with [`App.Meta.core_system_plugin_dirs`](https://cement.readthedocs.io/en/3.0/api/core/foundation/#cement.core.foundation.App.Meta.core_system_plugin_dirs) and [`App.Meta.core_user_plugin_dirs`](https://cement.readthedocs.io/en/3.0/api/core/foundation/#cement.core.foundation.App.Meta.core_user_plugin_dirs).  Default: `[]` |

## Working with Plugins

The plugin handler can be used to access information about loaded plugins, as well as manually loading plugins if necessary.

{% tabs %}
{% tab title="Example: Working with Extensions" %}
```python
from cement import App

with App('myapp') as app:
    # list loaded plugins
    app.plugin.get_loaded_plugins()

    # list enabled plugins
    app.plugin.get_enabled_plugins()

    # list disabled plugins
    app.plugin.get_disabled_plugins()

    # load a plugin
    app.plugin.load_plugin('myplugin')

    # load a list of plugins
    app.plugin.load_plugins(['myplugin1',
                             'myplugin2'])
```
{% endtab %}
{% endtabs %}

## Creating a Plugin

The plugin system is a mechanism for dynamically loading code to extend the functionality of a specific application. In general, this includes the registration of interfaces, handlers, and/or hooks but can include controllers, command-line options, or anything else.

The preferred method of creating a plugin would be via the included [developer tools](../getting-started/developer-tools.md):

```text
$ cement generate plugin /path/to/myapp/plugins
```

This will produce an example plugin directory like the following:

```text
├── __init__.py
├── controllers
│   ├── __init__.py
│   └── myplugin.py
└── templates
    ├── __init__.py
    └── plugins
        └── myplugin
            └── command1.jinja2
```

The example plugin includes a controller, sub-command, and output generated via [Jinja2](../extensions/jinja2.md) template. That said, the only thing Cement needs is a `load()` function.... everything else is arbitrary. In the generated plugin, we find this in `myplugin/__init__.py`:

```python
import os
from .controllers.myplugin import MyPlugin

def add_template_dir(app):
    path = os.path.join(os.path.dirname(__file__), 'templates')
    app.add_template_dir(path)

def load(app):
    app.handler.register(MyPlugin)
    app.hook.register('post_setup', add_template_dir)
```

{% hint style="info" %}
Plugins can provide anything from defining interfaces, registering hooks, or even adding command line sub-commands and arguments. The only thing required to make up a plugin is a `load()` function in `myplugin.py` or `myplugin/__init__.py` files.
{% endhint %}

You will notice that plugins are essentially the same as framework extensions. The difference is found both in when/how the code is loaded, as well as the purpose of that code.

{% hint style="info" %}
Framework extensions add functionality **to the framework** for the application to utilize, whereas application plugins **extend the functionality of the application** itself.
{% endhint %}

## Loading a Plugin

Plugin modules are discovered and loaded in the following order:

* From directories listed in `App.Meta.plugin_dirs`
* From the python path defined in `App.Meta.plugin_module`

In order for the framework to know about a plugin, it must be defined in the application's configuration settings under its designated section of `plugin.myplugin`. This configuration block can live in any application configuration file, including files loaded from configuration dirs \(ex: `/etc/myapp/plugin.d/myplugin.conf`\).

{% tabs %}
{% tab title="Example: Loading a Plugin" %}
{% code-tabs %}
{% code-tabs-item title="myapp.py" %}
```python
from cement import App

class MyApp(App):
    class Meta:
        label = 'myapp'
        plugin_dirs = ['./plugins']

with MyApp() as app:
    app.run()
```
{% endcode-tabs-item %}

{% code-tabs-item title="plugins/myplugin.py" %}
```python
def load(app):
    print('Inside MyPlugin!')
```
{% endcode-tabs-item %}
{% endcode-tabs %}
{% endtab %}

{% tab title="cli" %}
```text
$ python myapp.py
Inside MyPlugin!
...
```
{% endtab %}
{% endtabs %}

If a plugin configuration is found, its settings will be loaded into the app. However, the plugin will only be loaded if it is enabled:

```text
[myapp]
# ...

[plugin.myplugin]
enabled: true
```

## Single File Plugins vs. Plugin Directories

As of Cement 2.9.x, plugins can be either a single file \(i.e `myplugin.py`\) or a python module directory \(i.e. `myplugin/__init__.py`\). Both will be loaded and executed the exact same way.

One caveat, however, is that the submodules referenced from within a plugin directory must be relative paths. For example:

{% tabs %}
{% tab title="Example: Loading Submodules in a Plugin" %}
{% code-tabs %}
{% code-tabs-item title="myplugin/\_\_init\_\_.py" %}
```python
from .controllers import MyPluginController

def load(app):
    app.handler.register(MyPluginController)
```
{% endcode-tabs-item %}
{% endcode-tabs %}
{% endtab %}
{% endtabs %}

This will ensure that Python will properly load the sub-modules regardless of where they live on the filesystem \(or within a project's own modules, etc\).

## Loading Templates From Plugin Directories

In order for a plugin to use its own template files, its templates directory first needs to be registered with the app. We accomplish this with a `post_setup` hook:

{% tabs %}
{% tab title="Example: Registering Plugin Template Directories" %}
{% code-tabs %}
{% code-tabs-item title="myplugin/\_\_init\_\_.py" %}
```python
import os

def add_template_dir(app):
    path = os.path.join(os.path.basename(self.__file__, 'templates')
    app.add_template_dir(path)

​def load(app):
    app.hook.register('post_setup', add_template_dir)
```
{% endcode-tabs-item %}
{% endcode-tabs %}
{% endtab %}
{% endtabs %}

## Creating a Plugin Handler

All interfaces in Cement can be overridden with your own implementation. This can be done either by sub-classing [`PluginHandler`](https://cement.readthedocs.io/en/3.0/api/core/plugin/#cement.core.plugin.PluginHandler) itself, or by sub-classing an existing extension's handlers in order to alter their functionality.

{% tabs %}
{% tab title="Example: Creating a Plugin Handler" %}
{% code-tabs %}
{% code-tabs-item title="myapp.py" %}
```python
from cement import App
from cement.core.plugin import PluginHandler

class MyPluginHandler(PluginHandler):
    class Meta:
        label = 'my_plugin_handler'

    # do something to implement the interface

class MyApp(App):
    class Meta:
        label = 'myapp'
        plugin_handler = 'my_plugin_handler'
        handlers = [
            MyPluginHandler,
        ]
```
{% endcode-tabs-item %}
{% endcode-tabs %}
{% endtab %}
{% endtabs %}

