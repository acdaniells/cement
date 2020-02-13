# Mustache

## Introduction

The Mustache Extension provides output and file templating based on the [Mustache Templating Language](http://mustache.github.com/).

**Documentation References:**

* [Output Rendering](../core-foundation/output-rendering.md)
* [Templating](../core-foundation/templating.md)

**API References**

* [Cement Mustache Extension](https://cement.readthedocs.io/en/3.0/api/ext/ext_mustache/)
* [Mustache Library](http://mustache.github.io/)

## Requirements

* Pystache \(`pip install pystache`\)

## Configuration

### **Application Configuration Settings**

This extension honors the following settings under the primary namespace \(ex: `[myapp]`\) of the application configuration:

| **Setting** | **Description** |
| :--- | :--- |
| **template\_dir** | Directory path of a local template directory. |

### **Application Meta Options**

This extension honors the following [`App.Meta`](http://cement.readthedocs.io/en/3.0/api/core/foundation/?highlight=app.meta#cement.core.foundation.App.Meta) options:

| **Option** | **Description** |
| :--- | :--- |
| **template\_handler** | A template handler to use as the backend for templating |
| **template\_dirs** | A list of data directories to look for templates |
| **template\_module** | A python module to look for templates |

## Usage

### Output Handler

{% tabs %}
{% tab title="Example: Mustache Output Handler" %}
```python
from cement import App

class MyApp(App):
    class Meta:
        label = 'myapp'
        extensions = ['mustache']
        output_handler = 'mustache'

with MyApp() as app:
    app.run()

    # create some data
    data = {
        'foo': 'bar',
    }

    # render the data to STDOUT (default) via a template
    app.render(data, 'my_template.mustache')
```
{% endtab %}
{% endtabs %}

### **Template Handler**

{% tabs %}
{% tab title="Example: Using Mustache Template Handler" %}
```python
from cement import App

class MyApp(App):
    class Meta:
        label = 'myapp'
        extensions = ['mustache']
        template_handler = 'mustache'

with MyApp() as app:
    app.run()

    # create some data
    data = {
        'foo': 'bar'
    }

    # copy a source template directory to destination
    app.template.copy('/path/to/source/', 
                      '/path/to/destination/', 
                      data)

    # render any content as a template
    app.template.render('foo -> {{ foo }}', data)
```
{% endtab %}
{% endtabs %}

### Loading Partials

Mustache supports `partials`, or in other words template `includes`. These are also loaded by the output handler, but require a full file name. The partials will be loaded in the same way as the base templates.

{% tabs %}
{% tab title="Example: Using Mustache Partials" %}
{% code-tabs %}
{% code-tabs-item title="templates/base.mustache" %}
```python
Inside base.mustache
{{> partial.mustache}}
```
{% endcode-tabs-item %}

{% code-tabs-item title="templates/partial.mustache" %}
```text
Inside partial.mustache
```
{% endcode-tabs-item %}
{% endcode-tabs %}
{% endtab %}
{% endtabs %}

The above would output:

```text
Inside base.mustache
Inside partial.mustache
```

