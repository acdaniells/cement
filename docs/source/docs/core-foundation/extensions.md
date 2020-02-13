# Framework Extensions

## Introduction to the Extension Interface

Cement defines an [Extension Interface](https://cement.readthedocs.io/en/3.0/api/core/extension/#cement.core.extension.ExtensionInterface), as well as the default [CementExtensionHandler](https://cement.readthedocs.io/en/3.0/api/core/extension/#cement.core.extension.ExtensionHandler) that implements the interface. Its purpose is to manage loading framework extensions and making them usable by the application. Extensions are similar to [Application Plugins](plugins.md), but at the framework level \(application agnostic\).

{% hint style="warning" %}
Cement often includes multiple handler implementations of an interface that may or may not have additional features or functionality than the interface requires. The documentation below only references usage based on the interface and default handler \(not the full capabilities of an implementation\).
{% endhint %}

{% hint style="info" %}
As of Cement 2.1.3, optional extensions with external dependencies are now being shipped along with mainline sources. This means that although Cement Core continues to maintain a 100% zero dependency policy, Framework Extensions _can_ rely on external deps. It is the responsibility of the application developer to include these dependencies in their application \(as the Cement package does not include these dependencies\).
{% endhint %}

**API References:**

* [Cement Core Extension Module](https://cement.readthedocs.io/en/3.0/api/core/extension)

## Configuration

### Application Meta Options

The following options under [`App.Meta`](https://cement.readthedocs.io/en/3.0/api/core/foundation/#cement.core.foundation.App.Meta) modify extension handling:

| **Option** | **Description** |
| :--- | :--- |
| **extension\_handler** | A handler class that implements the Extension Interface.  This can be a string \(label of a registered handler\), an uninstantiated class, or an instantiated class object.  Default: [`ExtensionHandler`](https://cement.readthedocs.io/en/3.0/api/core/extension/#cement.core.extension.ExtensionHandler) |
| **extensions** | A list of additional framework extensions to load.  Will be merged together with [`App.Meta.core_extensions`](https://cement.readthedocs.io/en/3.0/api/core/foundation/#cement.core.foundation.App.Meta.core_extensions). |

## Working with Extensions

In general, extensions are only loaded and accessed by the framework. That said the extension handler can be used to access information about loaded extensions, as well as manually load extensions if necessary.

{% tabs %}
{% tab title="Example: Working with Extensions" %}
```python
from cement import App

with App('myapp') as app:
    # list loaded extensions
    app.ext.list()

    # load an extension
    app.ext.load_extension('myapp.ext.myextension')

    # load a list of extensions
    app.ext.load_extensions(['myapp.ext.ext1',
                             'myapp.ext.ext2'])
```
{% endtab %}
{% endtabs %}

## Creating an Extension

The extension system is a mechanism for dynamically loading code to extend the functionality of the framework. In general, this includes the registration of interfaces, handlers, and/or hooks but can include controllers, command-line options, or anything else.

The preferred method of creating an extension would be via the included [developer tools](../getting-started/developer-tools.md):

```text
$ cement generate extension /path/to/myapp/ext
```

This would produce something like the following:

{% tabs %}
{% tab title="Example: Creating an Extension" %}
{% code-tabs %}
{% code-tabs-item title="myapp/ext/ext\_myextension.py" %}
```python
from cement import minimal_logger

LOG = minimal_logger(__name__)

def myextension_pre_run_hook(app):
    # do something with app
    LOG.debug('Inside myextension_pre_run_hook!')

def load(app):
    # do something to extend cement
    app.hook.register('pre_run', myextension_pre_run_hook)
```
{% endcode-tabs-item %}
{% endcode-tabs %}
{% endtab %}
{% endtabs %}

{% hint style="info" %}
Extensions can provide anything from defining interfaces, registering hooks, or even adding command line arguments. The only thing required to make up an extension is the `load()` function.
{% endhint %}

You will notice that extensions are essentially the same as application plugins. The difference is found both in when/how the code is loaded, as well as the purpose of that code.

{% hint style="info" %}
Framework extensions add functionality **to the framework** for the application to utilize, whereas application plugins **extend the functionality of the application** itself.
{% endhint %}

## Loading Extensions

Extensions are loaded when [`App.setup()`](http://cement.readthedocs.io/en/3.0/api/core/foundation/#cement.core.foundation.App.setup) is called on an application. Cement automatically loads all extensions listed under the application's [`App.Meta.core_extensions`](http://cement.readthedocs.io/en/3.0/api/core/foundation/#cement.core.foundation.App.Meta.core_extensions) and [`App.Meta.extensions`](http://cement.readthedocs.io/en/3.0/api/core/foundation/#cement.core.foundation.App.Meta.extensions) meta options.

To load the above example into our application, we just add it to the list of `App.Meta.extensions`. Let's assume the extension code lives in `myapp/ext/ext_myextension.py`:

{% tabs %}
{% tab title="Example: Loading Extensions" %}
```python
from cement import App

class MyApp(App):
    class Meta:
        label = 'myapp'
        extensions = 'myapp.ext.ext_myextension'
```
{% endtab %}
{% endtabs %}

{% hint style="info" %}
Note that Cement provides a shortcut for its own builtin extensions so that you can refer to extensions via their short name \(ex: `json` instead of `cement.ext.ext_json`\). All other extensions must be referenced by their full dotted Python module name.
{% endhint %}

## Loading Extensions via a Configuration File

Some use cases may require that end-users be able to modify what framework extensions are loaded depending on the needs of the application, while most extensions are defined by the developer to support key features.

The following example demonstrates an application loading extensions defined via the `extensions` setting under the application's configuration settings.

{% tabs %}
{% tab title="Example: Loading Extensions via Configuration File" %}
{% code-tabs %}
{% code-tabs-item title="myapp.py" %}
```python
from cement import App

with App('myapp') as app:
    app.run()

    for e in app.extension.list():
        print(e)
```
{% endcode-tabs-item %}

{% code-tabs-item title="~/.myapp.conf" %}
```text
[myapp]
exensions = json, yaml, myapp.ext.ext_myextension
```
{% endcode-tabs-item %}
{% endcode-tabs %}
{% endtab %}

{% tab title="cli" %}
```text
$ python myapp.py
cement.ext.ext_dummy
cement.ext.ext_smtp
cement.ext.ext_plugin
cement.ext.ext_configparser
cement.ext.ext_logging
cement.ext.ext_argparse
cement.ext.ext_json
cement.ext.ext_yaml
myapp.ext.ext_myextension
```
{% endtab %}
{% endtabs %}

{% hint style="warning" %}
Note that extensions loaded in this way will happen **after** the config handler is setup. Normally, extensions are loaded just before the configuration files are read. Therefore, some extensions may not be compatible with this method if they attempt to perform any actions before `app.setup()` completes \(such as in early framework hooks before configuration files are loaded\).
{% endhint %}

