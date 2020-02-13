# Print

## Introduction

The Print Extension adds the [`PrintOutputHandler`](http://cement.readthedocs.io/en/3.0/api/ext/ext_print/#cement.ext.ext_print.PrintOutputHandler) and [`PrintDictOutputHandler`](http://cement.readthedocs.io/en/3.0/api/ext/ext_print/#cement.ext.ext_print.PrintDictOutputHandler) to render output in pure text. It is mostly intended for development, but also supports the additional `app.print()`extended function which can be used in place of the standard `print()` so that apps can continue to utilize features of the framework consistently \(such as honoring [`pre_render`](../core-foundation/hooks.md#pre_render) and [`post_render`](../core-foundation/hooks.md#post_render)hooks, etc\).

**Documentation References:**

* [Output Rendering](../core-foundation/output-rendering.md)

**API References:**

* [Cement Print Extension](https://cement.readthedocs.io/en/3.0/api/ext/ext_print/)

## Requirements

* No external dependencies

## Configuration

This extension does not support any application level configuration settings or meta options.

## Usage

{% tabs %}
{% tab title="Example: Using Print Output Handler" %}
```python
from cement import App

class MyApp(App):
    class Meta:
        label = 'myapp'
        extensions = ['print']

with MyApp() as app:
    app.run()
    app.print('This is an output message')
```
{% endtab %}
{% endtabs %}

Alternatively, you can use the `print_dict` output handler that can be useful in development as it simply just prints out a string representation of the data dict.

{% tabs %}
{% tab title="Example: Using Print Dict Output Handler" %}
```python
from cement import App

class MyApp(App):
    class Meta:
        label = 'myapp'
        extensions = ['print_dict']
        output_handler = 'print_dict'

with MyApp() as app:
    app.run()

    data = {
        'foo' : 'bar',
    }

    app.render(data)
```
{% endtab %}
{% endtabs %}

