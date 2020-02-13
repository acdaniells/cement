# Yaml

## Introduction

The Yaml Extension includes the [`YamlOutputHandler`](http://cement.readthedocs.io/en/3.0/api/ext/ext_yaml/#cement.ext.ext_yaml.YamlOutputHandler) to render output in pure Yaml, as well as the [`YamlConfigHandler`](http://cement.readthedocs.io/en/3.0/api/ext/ext_yaml/#cement.ext.ext_yaml.YamlConfigHandler) that allows applications to use Yaml configuration files as a drop-in replacement of the default [`ConfigParserConfigHandler`](https://cement.readthedocs.io/en/3.0/api/ext/ext_configparser/#cement.ext.ext_configparser.ConfigParserConfigHandler).

**Documentation References:**

* [Configuration Settings](../core-foundation/configuration-settings.md)
* [Output Rendering](../core-foundation/output-rendering.md)

**API References:**

* [Cement Yaml Extension](https://cement.readthedocs.io/en/3.0/api/ext/ext_yaml/)
* [Yaml Library](https://pyyaml.org/wiki/PyYAMLDocumentation)

## Requirements

* pyYaml \(`pip install pyYaml`\)

## Configuration

This extension does not support any application level configuration settings or meta options.

## Usage

### Config Handler

{% tabs %}
{% tab title="Example: Using Yaml Config Handler" %}
{% code-tabs %}
{% code-tabs-item title="myapp.py" %}
```python
from cement import App

class MyApp(App):
    class Meta:
        label = 'myapp'
        extensions = ['yaml']
        config_handler = 'yaml'
        config_file_suffix = '.yml'
```
{% endcode-tabs-item %}

{% code-tabs-item title="~/.myapp.yml" %}
```text
---
myapp:
    foo: bar
```
{% endcode-tabs-item %}
{% endcode-tabs %}
{% endtab %}
{% endtabs %}

### Output Handler

In general, you likely would not set `output_handler` to `yaml`, but rather another type of output handler that displays readable output to the end-user \(ex: Mustache, Jinja2, or Tabulate\). However, Cement supports overriding handlers via command line options if the [`Handler.Meta.overridable`](http://cement.readthedocs.io/en/3.0/api/core/handler/#cement.core.handler.Handler.Meta.overridable) option is set. For example, `-o yaml` will trigger the framework to use the `yaml` output handler, overriding the default set in [`App.Meta.output_handler`](http://cement.readthedocs.io/en/3.0/api/core/foundation/#cement.core.foundation.App.Meta.output_handler).

See the documentation on [Overriding Handlers via Command Line](../core-foundation/interfaces-and-handlers.md#overriding-handlers-via-command-line).

{% tabs %}
{% tab title="Example: Using Yaml Output Handler" %}
{% code-tabs %}
{% code-tabs-item title="myapp.py" %}
```python
from cement import App, init_defaults

META = init_defaults('output.yaml')
META['output.yaml']['overridable'] = True

class MyApp(App):
    class Meta:
        label = 'myapp'
        extensions = ['yaml', 'mustache']
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

$ python myapp.py -o yaml
{foo: bar}
```
{% endtab %}
{% endtabs %}

