# Miscellaneous

## Introduction to the Miscellaneous Utilities <a id="introduction-to-the-output-interface"></a>

Cement includes a Miscellaneous Utilities Module with helpers for common tasks that don't fit anywhere on their own.

**API References:**

* [​Cement Misc Utility Module​](https://cement.readthedocs.io/en/3.0/api/utils/misc/)

## Initialize Default Dictionaries

The included [`misc.init_defaults()`](https://cement.readthedocs.io/en/3.0/api/utils/misc/#cement.utils.misc.init_defaults) is used to initialize a defaults dictionary for configuration settings and meta options.

{% tabs %}
{% tab title="Example: Initialize Default Dictionaries" %}
```python
from cement.utils.misc import init_defaults

# create a dict with nested dicts
CONFIG = init_defaults('myapp', 
                       'log.logging', 
                       'output.json')

# setup the nested dicts
CONFIG['myapp']['foo'] = 'bar'
CONFIG['log.logging']['level'] = 'INFO'
CONFIG['output.json']['overridable'] = True
```
{% endtab %}
{% endtabs %}

{% hint style="info" %}
The `init_defaults` helper simply generates a dict with nested dicts of the given keys. It does not do anything special, but is used throughout the documentation as it generally makes things more readable in examples.

You can always use a standard `dict` for configuration and meta defaults, which often makes more sense when building larger applications with a lot of default settings to manage.
{% endhint %}

## Testing True Values

When reading configuration files and other unknown data sources, we often need to convert strings to boolean. For example, a setting of `true` read from a configparser text based config file will be a `str` type, but we want it as an `bool`.

The [`misc.is_true()`](https://cement.readthedocs.io/en/3.0/api/utils/misc/#cement.utils.misc.is_true) helper converts common `true` values to boolean.

{% tabs %}
{% tab title="Example: Testing True Values" %}
```python
from cement.utils.misc import is_true

# testing true values
is_true(1)
is_true('1')
is_true('true')
is_true('True')
is_true('TRUE')
is_true('yes')
is_true('on')
is_true(True)


# testing false values
is_true(0)
is_true('0')
is_true('false')
is_true('False')
is_true('FALSE')
is_true('no')
is_true('off')
is_true(False)
```
{% endtab %}
{% endtabs %}

## Minimal Logging

Cement provides a [`misc.minimal_logger()`](https://cement.readthedocs.io/en/3.0/api/utils/misc/#cement.utils.misc.minimal_logger) helper for use outside of the `App` object, most notably for extensions \(though they can use the application log also\). This should only be used by the framework, or when the application log is not available \(before application is setup maybe\).

{% tabs %}
{% tab title="Example: Minimal Logging" %}
```python
from cement.utils.misc import minimal_logger
LOG = minimal_logger('logging-namespace')
LOG.debug('This is a debug message')
```
{% endtab %}
{% endtabs %}

## Random Strings

The [`misc.rando()`](https://cement.readthedocs.io/en/3.0/api/utils/misc/#cement.utils.misc.rando) helper is available when a random string is necessary, generally used for testing purposes.

{% tabs %}
{% tab title="Example: Random Strings" %}
```python
from cement.utils.misc import rando

# create a random string (md5)
rando()

# add a salt
rando('anchG45jJfka')
```
{% endtab %}
{% endtabs %}

## Limit Text Line Length

When working with command lines, keeping output lines to less than 78 characters is a good best-practice. Cement provides the [`misc.wrap()`](https://cement.readthedocs.io/en/3.0/api/utils/misc/#cement.utils.misc.wrap) helper to accomplish this by adding a line break `\n`

{% tabs %}
{% tab title="Example: Limit Text Line Length" %}
```python
from cement.utils.misc import wrap

long = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis blandit cursus eros eget dictum. Curabitur eleifend nunc id eros consequat, vitae convallis quam sollicitudin. Nunc vitae efficitur lorem. Quisque facilisis imperdiet sem, nec facilisis elit faucibus non. Cras vitae interdum orci. Donec rutrum diam eget leo tincidunt, quis feugiat neque fermentum. Cras vel velit nibh. Phasellus porttitor, diam vitae ornare malesuada, mauris nulla ornare tortor, id congue tellus justo vel urna. Quisque tincidunt quis enim a bibendum. Donec sagittis nulla eu elit sollicitudin consequat."

# wrap with default 77 characters
res = wrap(long)
print(res)

# wrap with a total of 50 characters, and break long words / hyphens
res = wrap(long, width=50, long_words=True, hyphens=True)
print(res)
```
{% endtab %}

{% tab title="cli" %}
```text
$ python example.py

# default 77 characters

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis blandit cursus
eros eget dictum. Curabitur eleifend nunc id eros consequat, vitae convallis
quam sollicitudin. Nunc vitae efficitur lorem. Quisque facilisis imperdiet
sem, nec facilisis elit faucibus non. Cras vitae interdum orci. Donec rutrum
diam eget leo tincidunt, quis feugiat neque fermentum. Cras vel velit nibh.
Phasellus porttitor, diam vitae ornare malesuada, mauris nulla ornare tortor,
id congue tellus justo vel urna. Quisque tincidunt quis enim a bibendum.

# 50 characters and wrap long words or hyphens

Donec sagittis nulla eu elit sollicitudin consequat.
Lorem ipsum dolor sit amet, consectetur adipiscing
elit. Duis blandit cursus eros eget dictum.
Curabitur eleifend nunc id eros consequat, vitae
convallis quam sollicitudin. Nunc vitae efficitur
lorem. Quisque facilisis imperdiet sem, nec
facilisis elit faucibus non. Cras vitae interdum
orci. Donec rutrum diam eget leo tincidunt, quis
feugiat neque fermentum. Cras vel velit nibh.
Phasellus porttitor, diam vitae ornare malesuada,
mauris nulla ornare tortor, id congue tellus justo
vel urna. Quisque tincidunt quis enim a bibendum.
Donec sagittis nulla eu elit sollicitudin
consequat.
```
{% endtab %}
{% endtabs %}

