# Extending The App Object

The [`App.extend()`](https://cement.readthedocs.io/en/3.0/api/core/foundation/#cement.core.foundation.App.extend) method provides a mechanism that allows plugins, extensions, or the app itself to add objects or functions to the global application object.

For example, a plugin might extend the `App` with an `api` member allowing developers to call `app.api.get(...)`. The application itself does not provide `app.api`. However, the plugin does. As plugins are often third party, it is not possible for the plugin developer to simply sub-class the `App` class and add the functionality because the class is already instantiated by the time plugins are loaded.

{% tabs %}
{% tab title="Example: Extending the App Object" %}
```python
from cement import App

def example_func():
    print('Inside example_func')

def extend_myapp(app):
    app.extend('example', example_func)

class MyApp(App):
    class Meta:
        label = 'myapp'
        hooks = [
            ('post_setup', extend_myapp),
        ]

with MyApp() as app:
    app.run()

    # call the extended object or function
    app.example()
```

Alternatively from within an extension or plugin:

```python
def example_func():
    print('Inside example_func')

def extend_myapp(app):
    app.extend('example', example_func)

def load(app):
    app.hook.register('post_setup', extend_myapp)
```
{% endtab %}

{% tab title="cli" %}
```text
$ python test.py
Inside example_func
```
{% endtab %}
{% endtabs %}

{% hint style="info" %}
Extended members can be anything from instantiated objects to callables of any kind. Its use case is varied and arbitrary... but should be documented well by the developer that is extending it.
{% endhint %}

