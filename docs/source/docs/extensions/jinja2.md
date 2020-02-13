# Jinja2

## Introduction

The Jinja2 Extension provides the [`Jinja2OutputHandler`](http://cement.readthedocs.io/en/3.0/api/ext/ext_jinja2/#cement.ext.ext_jinja2.Jinja2OutputHandler) for output rendering, and the [`Jinja2TemplateHandler`](http://cement.readthedocs.io/en/3.0/api/ext/ext_jinja2/#cement.ext.ext_jinja2.Jinja2TemplateHandler) for file/content templating based on the Jinja2 templating language.

**Documentation References:**

* [Output Rendering](../core-foundation/output-rendering.md)
* [Templating](../core-foundation/templating.md)

**API References:**

* [Cement Jinja2 Extension](http://cement.readthedocs.io/en/3.0/api/ext/ext_jinja2/)
* [Jinja2 Module](http://jinja.pocoo.org/docs/2.10/api/)

## Requirements

* Jinja2 \(`pip install jinja2`\)

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

### **Output Handler**

{% tabs %}
{% tab title="Example: Using Jinja2 Output Handler" %}
```python
from cement import App

class MyApp(App):
    class Meta:
        label = 'myapp'
        extensions = ['jinja2']
        output_handler = 'jinja2'

with MyApp() as app:
    app.run()

    # create some data
    data = {
        'foo': 'bar',
    }

    # render the data to STDOUT (default) via a template
    app.render(data, 'my_template.jinja2')
```
{% endtab %}
{% endtabs %}

### **Template Handler**

{% tabs %}
{% tab title="Example: Using Jinja2 Template Handler" %}
```python
from cement import App

class MyApp(App):
    class Meta:
        label = 'myapp'
        extensions = ['jinja2']
        template_handler = 'jinja2'

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

