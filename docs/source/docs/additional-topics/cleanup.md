# Cleanup

## Introduction to Application Cleanup

The concept of cleanup after application run time is nothing new, but often ignored or forgotten by developers. What happens during cleanup all depends on the application. This might mean closing and deleting temporary files, removing session data, or deleting a PID \(Process ID\) file for example.

To allow for application cleanup not only within your program, but also external plugins and extensions, there is the [`app.close()`](https://cement.readthedocs.io/en/3.0/api/core/foundation/#cement.core.foundation.App.close) method that must be called after [`app.run()`](https://cement.readthedocs.io/en/3.0/api/core/foundation/#cement.core.foundation.App.run) regardless of any exceptions or runtime errors.

{% hint style="info" %}
When using the Python `with` operator, the `App.close()` method is automatically called when exiting the block.
{% endhint %}

Calling [`app.close()`](https://cement.readthedocs.io/en/3.0/api/core/foundation/#cement.core.foundation.App.close) ensures that the [`pre_close`](../core-foundation/hooks.md#cement-framework-hooks) and [`post_close`](../core-foundation/hooks.md#cement-framework-hooks) framework hooks are run, allowing extensions/plugins/etc to cleanup after the program runs.

## Exit Status and Error Codes

You can optionally configure your application to automatically call `sys.exit()` as well as set the status code that your application exists with via the meta option [App.Meta.exit\_on\_close](https://cement.readthedocs.io/en/3.0/api/core/foundation/#cement.core.foundation.App.Meta.exit_on_close) as well as setting `App.exit_code`:

{% tabs %}
{% tab title="Example: Exit Status and Error Codes" %}
```python
from cement import App

class MyApp(App):
    class Meta:
        label = 'myapp'
        exit_on_close = True

with MyApp() as app:
    try:
        app.run()
    except SomeException as e:
        # do something with e
        app.log.fatal('Caught Exception: %s' % e)
        app.exit_code = 100
```
{% endtab %}
{% endtabs %}

Note the use of the `App.exit_on_close` meta option. Cement **will not** call `sys.exit()` unless this is set to `True`. You will find that calling `sys.exit()` in testing is very problematic, therefore you will likely want to enable `exit_on_close` in production, but not for testing as in this example:

{% tabs %}
{% tab title="Example: Disable Exit on Close in Testing" %}
```python
# create a separate class for unit tests

class MyTestApp(MyApp):
    class Meta:
        exit_on_close = False
```
{% endtab %}
{% endtabs %}

{% hint style="info" %}
The default exit code is `0`. However, any uncaught exceptions will cause the application to exit with a code of `1` \(error\).
{% endhint %}

## Running Cleanup Code

Any extension, or plugin, or even the application itself that has cleanup code should do so within the `pre_close` or `post_close` framework hooks to ensure that it gets run.

{% tabs %}
{% tab title="Example: Running Cleanup Code" %}
```python
def my_cleanup_code(app):
    # do something to cleanup
    if os.path.exists('/path/to/some/dir'):
        os.remove('/path/to/some/dir')

def load(app):
    app.hook.register('pre_close', my_cleanup_code)
```
{% endtab %}
{% endtabs %}

