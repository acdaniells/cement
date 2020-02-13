# Json

## Introduction

The JSON Extension provides the [`JsonOutputHandler`](http://cement.readthedocs.io/en/3.0/api/ext/ext_json/#cement.ext.ext_json.JsonOutputHandler) for output rendering in pure JSON, as well as the [`JsonConfigHandler`](http://cement.readthedocs.io/en/3.0/api/ext/ext_json/#cement.ext.ext_json.JsonConfigHandler) that allows applications to use JSON configuration files as a drop-in replacement of the default [`ConfigParserConfigHandler`](http://cement.readthedocs.io/en/3.0/api/ext/ext_configparser/#cement.ext.ext_configparser.ConfigParserConfigHandler).

**Documentation References:**

* [Configuration Settings](../core-foundation/configuration-settings.md)
* [Output Rendering](../core-foundation/output-rendering.md)

**API References:**

* [Cement Json Extension](http://cement.readthedocs.io/en/3.0/api/ext/ext_json/)
* [Python Json Library](https://docs.python.org/3/library/json.html)

## Requirements

This extension does not have any external dependencies.

## Configuration

This extension does not rely on any application level configuration settings or meta options.

### Using an Alternative Json Module

In some edge cases users have wanted to use an alternative json module for performance reasons, in particular [UltraJson](https://github.com/esnme/ultrajson). It is possible to override the backend `json` library module to use, such as `ujson` or another **drop-in replacement** library. The recommended solution would be to override the [`JsonOutputHandler.Meta.json_module`](http://cement.readthedocs.io/en/3.0/api/ext/ext_json/#cement.ext.ext_json.JsonConfigHandler.Meta.json_module):

{% tabs %}
{% tab title="Example: Using an Alternative Json Module" %}
```python
from cement import App, init_defaults

META = init_defaults('output.json', 'config.json')
META['output.json']['json_module'] = 'ujson'
META['config.json']['json_module'] = 'ujson'

class MyApp(App):
    class Meta:
        label = 'myapp'
        extensions = ['json']
        meta_defaults = META
```
{% endtab %}
{% endtabs %}

## Usage

### Config Handler

{% tabs %}
{% tab title="Example: Using Json Config Handler" %}
{% code-tabs %}
{% code-tabs-item title="myapp.py" %}
```python
from cement import App

class MyApp(App):
    class Meta:
        label = 'myapp'
        extensions = ['json']
        config_handler = 'json'
        config_file_suffix = '.json'
```
{% endcode-tabs-item %}

{% code-tabs-item title="~/.myapp.json" %}
```text
{
    "myapp": {
        "foo": "bar"
    }
}
```
{% endcode-tabs-item %}
{% endcode-tabs %}
{% endtab %}
{% endtabs %}

### Output Handler

In general, you likely would not set `output_handler` to `json`, but rather another type of output handler that displays readable output to the end-user \(ex: Mustache, Jinja2, or Tabulate\). However, Cement supports overriding handlers via command line options if the [`Handler.Meta.overridable`](http://cement.readthedocs.io/en/3.0/api/core/handler/#cement.core.handler.Handler.Meta.overridable) option is set. For example, `-o json` will trigger the framework to use the `json` output handler, overriding the default set in [`App.Meta.output_handler`](http://cement.readthedocs.io/en/3.0/api/core/foundation/#cement.core.foundation.App.Meta.output_handler).

See the documentation on [Overriding Handlers via Command Line](../core-foundation/interfaces-and-handlers.md#overriding-handlers-via-command-line).

{% tabs %}
{% tab title="Example: Using Json Output Handler" %}
{% code-tabs %}
{% code-tabs-item title="myapp.py" %}
```python
from cement import App, init_defaults

META = init_defaults('output.json')
META['output.json']['overridable'] = True

class MyApp(App):
    class Meta:
        label = 'myapp'
        extensions = ['json', 'mustache']
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
$ python myapp.py
Foo: bar

$ python myapp.py -o json
{"foo": "bar"}
```
{% endtab %}
{% endtabs %}

