# Redis

## Introduction

The Redis Extension provides application caching and key/value store support via Redis.

Documentation References:

* [Caching](../core-foundation/caching.md)

API References:

* [Cement Redis Extension](https://cement.readthedocs.io/en/3.0/api/ext/ext_redis/)
* [Redis Library](https://redislabs.com/lp/python-redis/)

## Requirements

* Redis \(`pip install redis`\)

## Configuration

This extension honors the following config settings under a `[cache.redis]` section in any configuration file:

| **Setting** | **Description** |
| :--- | :--- |
| **expire\_time** | The default time in seconds to expire items in the cache.  Default: `0` \(does not expire\) |
| **host** | Redis server ip address or hostname |
| **port** | Redis server port |
| **db** | Redis server database id/namespace |

## Usage

{% tabs %}
{% tab title="Example: Using Redis Cache Handler" %}
{% code-tabs %}
{% code-tabs-item title="myapp.py" %}
```python
from cement import App, init_defaults

CONFIG = init_defaults('myapp', 'cache.redis')
CONFIG['cache.redis']['expire_time'] = 300 # seconds
CONFIG['cache.redis']['host'] = '127.0.0.1'
CONFIG['cache.redis']['port'] = 6379
CONFIG['cache.redis']['db'] = 0

class MyApp(App):
    class Meta:
        label = 'myapp'
        config_defaults = CONFIG
        extensions = ['redis']
        cache_handler = 'redis'

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
cache_handler = redis


[cache.redis]

# time in seconds that an item in the cache will expire
expire_time = 300

# Redis server
host = 127.0.0.1

# Redis port
port = 6379

# Redis database number
db = 0
```
{% endcode-tabs-item %}
{% endcode-tabs %}
{% endtab %}
{% endtabs %}

