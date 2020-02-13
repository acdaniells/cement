# Memcached

## Introduction

The Memcached Extension includes the [`MemcachedCacheHandler`](https://cement.readthedocs.io/en/3.0/api/ext/ext_memcached/#cement.ext.ext_memcached.MemcachedCacheHandler) and provides application caching and key/value store support via Memcached.

**Documentation References:**

* [Caching](../core-foundation/caching.md)

**API References:**

* [Cement Memcached Extension](https://cement.readthedocs.io/en/3.0/api/ext/ext_memcached/)
* [Pylibmc Library](http://sendapatch.se/projects/pylibmc/)

## Requirements

* Pylibmc \(`pip install pylibmc`\)
  * _There are known issues installing_ `pylibmc` _on macOS/Homebrew via PIP._  [_This post might be helpful_](http://stackoverflow.com/questions/14803310/error-when-install-pylibmc-using-pip)_._

## Configuration

This extension honors the following config settings under a `[cache.memcached]` section in any configuration file:

| **Setting** | **Description** |
| :--- | :--- |
| **expire\_time** | The default time in seconds to expire items in the cache.  Default: `0` \(does not expire\) |
| **hosts** | List of memcached servers \(comma separated if using a plain text based config handler like configparser\). |

## Usage

{% tabs %}
{% tab title="Example: Using Memcached Cache Handler" %}
{% code-tabs %}
{% code-tabs-item title="myapp.py" %}
```python
from cement import App
from cement.utils.misc import init_defaults

CONFIG = init_defaults('myapp', 'cache.memcached')
CONFIG['cache.memcached']['expire_time'] = 300 # seconds
CONFIG['cache.memcached']['hosts'] = ['127.0.0.1']

class MyApp(App):
    class Meta:
        label = 'myapp'
        config_defaults = CONFIG
        extensions = ['memcached']
        cache_handler = 'memcached'

with MyApp() as app:
    # Run the app
    app.run()

    # Set a cached value
    app.cache.set('my_key', 'my value')

    # Get a cached value
    app.cache.get('my_key')

    # Delete a cached value
    app.cache.delete('my_key')

    # Delete the entire cache
    app.cache.purge()
```
{% endcode-tabs-item %}

{% code-tabs-item title="~/.myapp.conf" %}
```text
[myapp]

# set the cache handler to use
cache_handler = memcached


[cache.memcached]

# time in seconds that an item in the cache will expire
expire_time = 3600

# comma seperated list of memcached servers
hosts = 127.0.0.1, cache.example.com
```
{% endcode-tabs-item %}
{% endcode-tabs %}
{% endtab %}
{% endtabs %}

