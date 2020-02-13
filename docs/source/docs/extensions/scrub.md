# Scrub

## Introduction

The Scrub Extension provides an easy mechanism for obfuscating sensitive information from command line output. It is useful for debugging and for providing end-user output to developers without including sensitive info like IP addresses, phone numbers, credit card numbers, etc.

Scrubbing happens in a [`post_render`](../core-foundation/hooks.md#pre_render) hook by iterating over the list of tuples in `App.Meta.scrub`and calling `re.sub()` on the text provided by the output handler in use. Therefore, all output produced by `app.render()` will be scrubbed… including JSON, YAML, or any other output handler.

**API References:**

* [Cement Scrub Extension](https://cement.readthedocs.io/en/3.0/api/ext/ext_scrub/)

## **Requirements**

* No external dependencies

## **Configuration**

### Application Configuration Settings

This extension does not rely on any application level configuration settings or meta options.

### **Application Meta Data**

This extension honors the following `App.Meta` options:

| Option | **Description** |
| :--- | :--- |
| **scrub** | A list of tuples in the form of `[ ( 'REGEX', 'REPLACEMENT' ) ]` |

## **Usage**

{% tabs %}
{% tab title="Example: Using Scrub Extension" %}
```python
from cement import App

class MyApp(App):
    class Meta:
        label = 'myapp'
        extensions = ['scrub', 'print']
        scrub = [
            # obfuscate ipv4 addresses
            (r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", '***.***.***.***'),
        ]

with MyApp() as app:
    app.run()
    app.print('This is an IPv4 Address: 192.168.1.100')
```
{% endtab %}

{% tab title="cli" %}
```text
$ python myapp.py
This is an IPv4 Address: 192.168.1.100

$ python myapp.py --scrub
This is an IPv4 Address: ***.***.***.***
```
{% endtab %}
{% endtabs %}

{% hint style="warning" %}
In order for scrubbing to work, output must be rendered via a registered [output handler](../core-foundation/output-rendering.md). If only printing to console is desired, use the `print` extension along with `app.print()` \(as in the above example\).
{% endhint %}

