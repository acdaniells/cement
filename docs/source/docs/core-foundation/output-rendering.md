# Output Rendering

## Introduction to the Output Interface

Cement defines an [Output Interface](https://cement.readthedocs.io/en/3.0/api/core/output/#cement.core.output.OutputInterface), as well as the default [DummyOutputHandler](https://docs.builtoncement.com/{{%20version%20}}/api/ext/ext_dummy.html) that implements the interface as a placeholder but does not actually produce any output.

{% hint style="warning" %}
Cement often includes multiple handler implementations of an interface that may or may not have additional features or functionality than the interface requires. The documentation below only references usage based on the interface and default handler \(not the full capabilities of an implementation\).
{% endhint %}

**Cement Extensions That Provide Output Handlers:**

* [Dummy](../extensions/dummy.md)
* [Json](../extensions/json.md)
* [Yaml](../extensions/yaml.md)
* [Jinja2](../extensions/jinja2.md)
* [Mustache](../extensions/mustache.md)
* [Tabulate](../extensions/tabulate.md)

**API References:**

* [Cement Core Output Module](https://cement.readthedocs.io/en/3.0/api/core/output)

## **Configuration**

### **Application Meta Options**

The following options under [`App.Meta`](https://cement.readthedocs.io/en/3.0/api/core/foundation/#cement.core.foundation.App.Meta) modify configuration handling:

| **Option** | **Description** |
| :--- | :--- |
| **output\_handler** | The handler that implements the output interface. |

## Rending Output

Cement applications do not need to use an output handler by any means. Most small applications can get away with simple `print()` statements. However, anyone who has ever built a bigger application that produces a lot of output will know that this can get ugly very quickly in your code.

Using an output handler allows the developer to keep their logic clean, and offload the display of relevant data to an output handler, possibly by templates or other means \(GUI?\).

An output handler has a `render()` function that takes a data dictionary to produce output. Some output handlers may also accept a `template` or other parameters that define how output is rendered. This is easily accessible by the application object.

{% tabs %}
{% tab title="Example: Rendering Output" %}
```python
from cement import App

with App('myapp' as app:
    app.run()

    # create a data dictionary
    data = {
        'foo': 'bar',
    }

    # render data dictionary
    app.render(data)
```
{% endtab %}
{% endtabs %}

The above example uses the default `dummy` output handler, therefore nothing is displayed on screen. That said, for an example we can use the JSonOutputHandler to see something happen:

{% tabs %}
{% tab title="Example: Defining an Output Handler" %}
```python
from cement import App

class MyApp(App):
    class Meta:
        label = 'myapp'
        extensions = ['json']
        output_handler = 'json'

with MyApp() as app:
    app.run()

    # create a data dictionary
    data = {
        'foo': 'bar',
    }

    # render data dictionary
    app.render(data)
```
{% endtab %}

{% tab title="cli" %}
```text
$ python myapp.py
{"foo": "bar"}
```
{% endtab %}
{% endtabs %}

## Rendering Output via Templates

While some output handlers only require the `data` dictionary, others can utilize text templates to render formatted output to console.

{% tabs %}
{% tab title="Example: Rendering Output via Templates" %}
{% code-tabs %}
{% code-tabs-item title="myapp.py" %}
```python
from cement import App

class MyApp(App):
    class Meta:
        label = 'myapp'
        extensions = ['jinja2']
        output_handler = 'jinja2'
        template_dir = './templates'

with MyApp() as app:
    app.run()

    # create a data dictionary
    data = {
        'foo': 'bar',
    }

    # render data dictionary
    app.render(data, 'example.jinja2')
```
{% endcode-tabs-item %}

{% code-tabs-item title="templates/example.jinja2" %}
```text
Example Jinja2 Template

{% if foo %}
    Foo => {{ foo }}
{% endif %}
```
{% endcode-tabs-item %}
{% endcode-tabs %}
{% endtab %}

{% tab title="cli" %}
```text
$ python myapp.py
Example Jinja2 Template

    Foo => bar
```
{% endtab %}
{% endtabs %}

## Template Directory Loading

Template directories are looked for in the most common places by default as defined by [`App.Meta.template_dirs`](https://cement.readthedocs.io/en/3.0/api/core/foundation/#cement.core.foundation.App.Meta.template_dirs):

* ~/.myapp/templates
* ~/.config/myapp/templates
* /usr/lib/myapp/templates

{% hint style="info" %}
End-users can prepend their own paths to this list by setting the `template_dir` setting under the application configuration settings.
{% endhint %}

Once a template is found, loading stops and the template is rendered.

## Creating an Output Handler

All interfaces in Cement can be overridden with your own implementation. This can be done either by sub-classing [`OutputHandler`](https://cement.readthedocs.io/en/3.0/api/core/output/#cement.core.output.OutputHandler) itself, or by sub-classing an existing extension's handlers in order to alter their functionality.

{% tabs %}
{% tab title="Example: Creating an Output Handler" %}
{% code-tabs %}
{% code-tabs-item title="myapp.py" %}
```python
from cement import App
from cement.core.output import OutputHandler

class MyOutputHandler(OutputHandler):
    class Meta:
        label = 'my_output_handler'

    # do something to implement the interface

class MyApp(App):
    class Meta:
        label = 'myapp'
        output_handler = 'my_output_handler'
        handlers = [
            MyOutputHandler,
        ]
```
{% endcode-tabs-item %}
{% endcode-tabs %}
{% endtab %}
{% endtabs %}

