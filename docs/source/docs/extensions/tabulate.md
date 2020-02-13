# Tabulate

## Introduction

The Tabulate Extension includes the [`TabulateOutputHandler`](https://cement.readthedocs.io/en/3.0/api/ext/ext_tabulate/#cement.ext.ext_tabulate.TabulateOutputHandler), and provides output handling based on the [Tabulate](https://pypi.python.org/pypi/tabulate) library. Its format is familiar to users of MySQL, Postgres, etc.

**Documentation References:**

* [Output Rendering](../core-foundation/output-rendering.md)

**API References:**

* [Cement Tabulate Extension](https://cement.readthedocs.io/en/3.0/api/ext/ext_tabulate)
* [Tabulate Library](https://github.com/gregbanks/python-tabulate)

## Requirements

* Tabulate \(`pip install tabulate`\)

## Configuration

This extension does not support any application level configuration settings or meta options.

## Usage

{% tabs %}
{% tab title="Example: Using Tabulate Output Handler" %}
{% code-tabs %}
{% code-tabs-item title="myapp.py" %}
```python
from cement import App

class MyApp(App):
    class Meta:
        label = 'myapp'
        extensions = ['tabulate']
        output_handler = 'tabulate'

with MyApp() as app:
    app.run()

    # create a dataset
    headers = ['NAME', 'AGE', 'ADDRESS']
    data = [
        ["Krystin Bartoletti", 47, "PSC 7591, Box 425, APO AP 68379"],
        ["Cris Hegan", 54, "322 Reubin Islands, Leylabury, NC 34388"],
        ["George Champlin", 25, "Unit 6559, Box 124, DPO AA 25518"],
        ]

    app.render(data, headers=headers)
```
{% endcode-tabs-item %}
{% endcode-tabs %}
{% endtab %}

{% tab title="cli" %}
```text
$ python myapp.py
| NAME               | AGE | ADDRESS                                 |
|--------------------+-----+-----------------------------------------|
| Krystin Bartoletti |  47 | PSC 7591, Box 425, APO AP 68379         |
| Cris Hegan         |  54 | 322 Reubin Islands, Leylabury, NC 34388 |
| George Champlin    |  25 | Unit 6559, Box 124, DPO AA 25518        |
```
{% endtab %}
{% endtabs %}

