# Hooks

## Introduction to Hooks

Hooks allow developers to tie into different pieces of the framework and an application.

A hook can be defined anywhere, be it internally in the application, or in a plugin, extension, etc. Once a hook is defined, functions can be registered to that hook so that when the hook is called, all functions registered to that hook will be run. By defining a hook, you are saying that you are going to honor that hook somewhere in your application. Using descriptive hook names are good for clarity. For example, `pre_database_connect` is obviously a hook that will be run before a database connection is attempted.

{% hint style="info" %}
The most important thing to remember when defining hooks for your application is to properly document them. Include whether anything is expected in return or what, if any, arguments will be passed to the hook functions when called.
{% endhint %}

**API Reference:**

* ​[Cement Hook Module](https://docs.builtoncement.com/{{%20version%20}}/api/core/hook.html)​

## **Configuration**

### **Application Meta Options**

The following options under [`App.Meta`](https://cement.readthedocs.io/en/3.0/api/core/foundation/#cement.core.foundation.App.Meta) modify hook handling:

| **Option** | **Description** |
| :--- | :--- |
| **define\_hooks** | List of hook labels to define hooks by. |
| **hooks** | List of hooks to be registered. |

## Working with Hooks

The [`HookManager`](https://cement.readthedocs.io/en/3.0/api/core/hook/#cement.core.hook.HookManager) provides mechanisms for defining, registering, and executing hooks.

{% tabs %}
{% tab title="Example: Working with Hooks" %}
```python
from cement import App

def some_function():
    pass

with App('myapp') as app:
    # list all defined hooks
    app.hook.list()

    # define a hook
    app.hook.define('my_example_hook')

    # test if a hook is defined
    app.hook.defined('my_example_hook')

    # register a function to a hook
    app.hook.register('my_example_hook', some_function)

    # run a hook
    for res in app.hook.run('my_example_hook'):
        # do something with res...
        pass
```
{% endtab %}
{% endtabs %}

## Defining a Hook

A hook can be defined anywhere. However it is generally recommended to define the hook as early as possible. A hook definition simply gives a label to the hook, and allows the developer \(or third-party plugin developers\) to register functions to that hook. Its label is arbitrary.

The most convenient way to define a hook is via [`CementApp.Meta.define_hooks`](https://cement.readthedocs.io/en/3.0/api/core/foundation/#cement.core.foundation.App.Meta.define_hooks):

{% tabs %}
{% tab title="Example: Defining Hooks via App" %}
```python
from cement import App

class MyApp(App):
    class Meta:
        label = 'myapp'
        define_hooks = [
            'my_example_hook',
        ]
```
{% endtab %}
{% endtabs %}

Alternatively, hooks can be defined by extensions or plugins via the hook manager directly:

{% tabs %}
{% tab title="Example: Defining Hooks via Extensions/Plugins" %}
```python
def load(app):
    app.hook.define('my_example_hook')
```
{% endtab %}
{% endtabs %}

## Registering Functions to a Hook

A hook is just an identifier, but the functions registered to that hook are what get run when the hook is called. Registering a hook function should also be done early on in the runtime process, any time after the application has been created, after the hook is defined, and before the hook is run. Note that every hook is different, and therefore should be clearly documented by the owner of the hook \(application developer, plugin developer, etc\).

The most convenient way to register a hook function is via [`CementApp.Meta.hooks`](https://cement.readthedocs.io/en/3.0/api/core/foundation/#cement.core.foundation.App.Meta.hooks):

{% tabs %}
{% tab title="Example: Registering Functions to a Hook" %}
```python
from cement import App

def my_hook_function(app):
    # do something with app
    pass

class MyApp(App):
    class Meta:
        label = 'myapp'
        hooks = [
            ('pre_setup', my_hook_function),
        ]
```
{% endtab %}
{% endtabs %}

Alternatively, hooks can be registered by extensions or plugins via the hook manager directly:

{% tabs %}
{% tab title="Example: Registering Hooks via Extensions/Plugins" %}
```python
def my_hook_function(app):
    # do something with app
    pass

def load(app):
    app.hook.register('pre_setup', my_hook_function)
```
{% endtab %}
{% endtabs %}

## Hook Parameters and Return Values

What you receive from a hook \(arguments, keyword arguments\), and what you return from your hook function depends on what the developer who owns the hook has defined. Each hook is different, and the nature of the hook determines whether you need to accept arguments, or return anything.

{% hint style="warning" %}
It is important that the owner of the hook \(application/plugin developer, etc\) properly document the usage of the hook including the `*args`, `**kwargs` it is sending as well as what it is expecting in return.
{% endhint %}

## Running a hook

Now that a hook is defined, and functions have been registered to that hook all that is left is to run it. Keep in mind, you don't want to run a hook until after the application load process... meaning, after all plugins and other code are loaded. If you receive an error that the hook doesn't exist, then you are likely trying to register a hook too soon before the hook is defined. Likewise, if it doesn't seem like your hook is running and you don't see it mentioned in `--debug` output, you might be registering your hook **after** the hook has already run.

{% tabs %}
{% tab title="Example: Running a Hook" %}
```python
from cement import App

class MyApp(App):
    class Meta:
        label = 'myapp'
        define_hooks = ['my_example_hook']

with MyApp() as app:
    for res in app.hook.run('my_example_hook'):
        # do something with res
        pass
```
{% endtab %}
{% endtabs %}

As you can see we iterate over the hook, rather than just calling `app.hook.run()` by itself. This is necessary because `app.hook.run()` yields the results from each hook function as they are run. Hooks can be run anywhere _after_ the hook is defined, and hooks are registered to that hook.

## Controlling Hook Run Order

Sometimes you might have a very specific purpose in mind for a hook, and need it to run before or after other functions in the same hook. For that reason there is an optional `weight` parameter that can be passed when registering a hook function.

{% tabs %}
{% tab title="Example: Controlling Hook Run Order" %}
```python
from cement import App

def func1(app):
    print('Inside func1()')

def func2(app):
    print('Inside func2()')

def func3(app):
    print('Inside func3()')


class MyApp(App):
    class Meta:
        label = 'myapp'

        hooks = [
            ('pre_setup', func1, 0),
            ('pre_setup', func2, 100),
            ('pre_setup', func3, -99),
        ]

with MyApp() as app:
    app.run()
```
{% endtab %}

{% tab title="cli" %}
```text
$ python tmp/myapp.py
Inside func3()
Inside func1()
Inside func2()
```
{% endtab %}
{% endtabs %}

As you can see, it doesn’t matter what order we register the hook, the weight runs them in order from lowest to highest based on their `weight` value.

Alternatively, with a plugin or extension:

{% tabs %}
{% tab title="Example: Controlling Hook Run Order via Extension/Plugin" %}
```python
def func1():
    pass

def load(app):
    app.hook.register('my_example_hook', func1, weight=10)
```
{% endtab %}
{% endtabs %}

## Cement Framework Hooks

Cement defines a number of hooks that tie into the framework.

| **Hook Name** | **Description** |
| :--- | :--- |
| **pre\_setup** | Run first when `App.setup()` is called. The application object is passed as an argument.  Nothing is expected in return. |
| **post\_setup** | Run last when `App.setup()` is called. The application object is passed as an argument. Nothing is expected in return. |
| **pre\_run** | Run first when `App.run()` is called. The application object is passed as an argument. Nothing is expected in return. |
| **post\_run** | Run last when `App.run()` is called. The application object is passed as an argument. Nothing is expected in return. |
| **pre\_argument\_parsing** | Run after `App.run()` is called, just _before_ argument parsing happens. The application object is passed as an argument to these hook functions. Nothing is expected in return. |
| **post\_argument\_parsing** | Run after `App.run()` is called, just _after_ argument parsing happens. The application object is passed as an argument to these hook functions. Nothing is expected in return.This hook is generally useful where the developer needs to perform actions based on the arguments that were passed at command line, but before the logic of `App.run()` happens. |
| **pre\_render** | Run first when `App.render()` is called. The application object, and data dictionary are passed as arguments. Must return either the original data dictionary, or a modified one. |
| **post\_render** | Run last when `App.render()` is called. The application object, and rendered output text are passed as arguments. Must return either the original output text, or a modified version. |
| **pre\_close** | Run first when `App.close()` is called. This hook should be used by plugins and extensions to do any 'cleanup' at the end of program execution. Nothing is expected in return. |
| **post\_close** | Run last when `App.close()` is called. Most use cases need `pre_close`, however this hook is available should anyone need to do anything after all other cleanup operations. |
| **signal** | Run when signal handling is enabled, and the defined signal handler callback is executed. This hook should be used by the application, plugins, and extensions to perform any actions when a specific signal is caught. Nothing is expected in return. |

