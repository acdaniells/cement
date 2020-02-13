# Dummy

## Introduction

The Dummy Extension provides several placeholder type handlers to either mock operations or provide local-only usage during development. A perfect example is the [`DummyMailHandler`](http://cement.readthedocs.io/en/3.0/api/ext/ext_dummy/#cement.ext.ext_dummy.DummyMailHandler) that can be use during development or staging to prevent real email messages from being sent externally.

**API References:**

* [Cement Dummy Extension](http://cement.readthedocs.io/en/3.0/api/ext/ext_dummy/)

## Requirements

* No external dependencies

## Configuration

**DummyMailHandler**

This extension supports the following configuration settings under a `[mail.dummy]` configuration section:

| **Setting** | **Description** |
| :--- | :--- |
| **to** | Default recipient address \(list, or comma separated depending on the config handler in use\). |
| **from\_addr** | Default sender address |
| **cc** | Default carbon-copy addresses \(list, or comma separated depending on the config handler in use\) |
| **bcc** | Default blind-carbon-copy addresses \(list, or comma separated depending on the config handler in use\) |
| **subject** | Default subject line |
| **subject\_prefix** | Additional string to prepend to the subject line of all messages |

## Usage

{% tabs %}
{% tab title="Example: Using Dummy Extension" %}
```python
from cement import App

class MyApp(App):
    class Meta:
        label = 'myapp'
        extensions = ['dummy']
        output_handler = 'dummy'
        template_handler = 'dummy'
        mail_handler = 'dummy'

with MyApp() as app:
    app.run()
```
{% endtab %}
{% endtabs %}

