# Generate

## Introduction

The Generate Extension includes the [Generate](https://cement.readthedocs.io/en/3.0/api/ext/ext_generate/#cement.ext.ext_generate.Generate) controller, and provides a mechanism for generating common content from template directories. An example use case would be the ability for application developers to easily generate new plugins for their application… similar in other applications such as Chef Software’s `chef generate cookbook` type utilities.

The [Cement Developer Tools](../getting-started/developer-tools.md) use this extension to generate projects, plugins, extensions, scripts, etc for developers building their applications on the framework.

**Documentation References:**

* [Templating](../core-foundation/templating.md)

**API References:**

* [Cement Generate Extension](http://cement.readthedocs.io/en/3.0/api/ext/ext_generate/)

## **Requirements**

* pyYaml \(`pip install pyYaml`\)
* A valid [template handler](../core-foundation/templating.md) must be defined at the application level via [`App.Meta.template_handler`](http://cement.readthedocs.io/en/3.0/api/core/foundation/#cement.core.foundation.App.Meta.template_handler) such as `jinja2`, `mustache`, etc.

## **Configuration**

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

## **Usage**

### **Examples**

{% tabs %}
{% tab title="Example: Using Generate Extension" %}
```python
from cement import App

class MyApp(App):
    class Meta:
        label = 'myapp'
        extensions = ['generate', 'jinja2']
        template_handler = 'jinja2'


with MyApp() as app:
    app.run()
```
{% endtab %}

{% tab title="cli" %}
```text
$ python myapp.py --help
usage: myapp [-h] [--debug] [--quiet] {generate} ...

optional arguments:
  -h, --help  show this help message and exit
  --debug     toggle debug output
  --quiet     suppress all output

sub-commands:
  {generate}
    generate  generate controller


$ python myapp.py generate --help
usage: myapp generate [-h] {plugin} ...

optional arguments:
  -h, --help  show this help message and exit

sub-commands:
  {plugin}
    plugin      generate plugin from template
```
{% endtab %}
{% endtabs %}

### **Generate Templates**

The Generate Extension looks for a `generate` sub-directory in all defined template directory paths defined at the application level. If it finds a `generate` directory it treats all items within that directory as a generate template.

A Generate Template requires a single configuration YAML file called `.generate.yml` that looks something like:

```yaml
---
ignore:
    - "^(.*)ignore-this(.*)$"
    - "^(.*)ignore-that(.*)$"

exclude:
    - "^(.*)exclude-this(.*)$"
    - "^(.*)exclude-that(.*)$"

variables:
    - name: 'my_variable_name'
      prompt: 'The Prompt Displayed to The User'
```

**Generate Template Configuration**

The following configurations are supported in a generate template’s config:

| **ignore** | A list of regular expressions to match files that you want to completely ignore |
| :--- | :--- |
| **exclude** | A list of regular expressions to match files that you want to copy only \(not rendered as template\) |
| **variables** | A list of variable definitions that support the following sub-keys: |

