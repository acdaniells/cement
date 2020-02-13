# Templating

## Introduction to the Template Interface <a id="introduction-to-the-output-interface"></a>

Cement defines a [Template Interface](https://cement.readthedocs.io/en/3.0/api/core/template/#cement.core.template.TemplateInterface), as well as a default [`DummyTemplateHandler`](https://cement.readthedocs.io/en/3.0/api/ext/ext_dummy/#cement.ext.ext_dummy.DummyTemplateHandler) that implements the interface as a placeholder but does not actually do anything.

{% hint style="warning" %}
Cement often includes multiple handler implementations of an interface that may or may not have additional features or functionality than the interface requires. The documentation below only references usage based on the interface and default handler \(not the full capabilities of an implementation\).
{% endhint %}

\*\*\*\*

**Cement Extensions That Provide Template Handlers:**

* ​[Jinja2](../extensions/jinja2.md)
* [Mustache](../extensions/mustache.md)
* [Dummy](../extensions/dummy.md)

**API References:**

* [​Cement Core Template Module​](https://cement.readthedocs.io/en/3.0/api/core/template)

## **Configuration** <a id="configuration"></a>

### **Application Meta Options** <a id="application-meta-options"></a>

The following options under [`App.Meta`](https://cement.readthedocs.io/en/3.0/api/core/foundation/#cement.core.foundation.App.Meta) modify configuration handling:

| **Option** | **Description** |
| :--- | :--- |
| **template\_handler** | The handler that implements the template interface. |

## Working with Templates

The template handler can be used to render content in-line, as well as copy render source directories before copying them to their destination.

{% tabs %}
{% tab title="Example: Working with Templates" %}
```python
from cement import App

class MyApp(App):
    class Meta:
        label = 'myapp'
        extensions = ['jinja2']
        template_handler = 'jinja2'

with MyApp() as app:
    # create a data dictionary for templating
    data = {
        'foo': 'bar'
    }

    # render content as template
    app.template.render('Foo => {{ foo }}', data)

    # render and copy a source directory
    src = '/path/to/source/dir'
    dst = '/path/to/destination/dir'
    app.template.copy(src, dst, data)
```
{% endtab %}
{% endtabs %}

{% hint style="info" %}
When copying a source directory, both the file/directory path names themselves are rendered as templates as well as the contents of files.
{% endhint %}

## Creating a Template Handler

All interfaces in Cement can be overridden with your own implementation. This can be done either by sub-classing [`TemplateHandler`](https://cement.readthedocs.io/en/3.0/api/core/template/#cement.core.template.TemplateHandler) itself, or by sub-classing an existing extension's handlers in order to alter their functionality.

{% tabs %}
{% tab title="Example: Creating a Template Handler" %}
{% code-tabs %}
{% code-tabs-item title="myapp.py" %}
```python
from cement import App
from cement.core.template import TemplateHandler

class MyTemplateHandler(TemplateHandler):
    class Meta:
        label = 'my_template_handler'

    # do something to implement the interface

class MyApp(App):
    class Meta:
        label = 'myapp'
        template_handler = 'my_template_handler'
        handlers = [
            MyTemplateHandler,
        ]
```
{% endcode-tabs-item %}
{% endcode-tabs %}
{% endtab %}
{% endtabs %}

