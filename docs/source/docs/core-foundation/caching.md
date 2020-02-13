# Caching

## Introduction to the Cache Interface

Cement defines a [Cache Interface](https://cement.readthedocs.io/en/3.0/api/core/cache/#cement.core.cache.CacheInterface), but does not implement caching by default.

{% hint style="warning" %}
Cement often includes multiple handler implementations of an interface that may or may not have additional features or functionality than the interface requires. The documentation below only references usage based on the interface and default handler \(not the full capabilities of an implementation\).
{% endhint %}

**Cement Extensions That Provide Cache Handlers:**

* [Memcached](../extensions/memcached.md)
* [Redis](../extensions/redis.md)

**API References:**

* [Cement Core Cache Module](https://cement.readthedocs.io/en/3.0/api/core/cache)

## **Configuration**

### **Application Meta Options**

The following options under [`App.Meta`](https://cement.readthedocs.io/en/3.0/api/core/foundation/#cement.core.foundation.App.Meta) modify configuration handling:

| **Option** | **Description** |
| :--- | :--- |
| **cache\_handler** | The handler that implements the cache interface. |

## Working with Caches

The following example uses the [Memcached Extension](../extensions/memcached.md), which requires the `pylibmc` library to be installed, as well as a Memcached server running on `localhost:11211`.

{% tabs %}
{% tab title="Example: Working with Caches" %}
```python
from cement import App
from cement.utils.misc import init_defaults

CONFIG = init_defaults('myapp', 'memcached')
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
{% endtab %}
{% endtabs %}

## Creating a Cache Handler

All interfaces in Cement can be overridden with your own implementation. This can be done either by sub-classing [`CacheHandler`](https://cement.readthedocs.io/en/3.0/api/core/cache/#cement.core.cache.CacheHandler) itself, or by sub-classing an existing extension's handlers in order to alter their functionality.

{% tabs %}
{% tab title="Example: Creating a Cache Handler" %}
{% code-tabs %}
{% code-tabs-item title="myapp.py" %}
```python
from cement import App
from cement.core.cache import CacheHandler

class MyCacheHandler(CacheHandler):
    class Meta:
        label = 'my_cache_handler'

    # do something to implement the interface

class MyApp(App):
    class Meta:
        label = 'myapp'
        cache_handler = 'my_cache_handler'
        handlers = [
            MyCacheHandler,
        ]
```
{% endcode-tabs-item %}
{% endcode-tabs %}
{% endtab %}
{% endtabs %}

