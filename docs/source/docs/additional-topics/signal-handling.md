# Signal Handling

## Introduction to Signal Handling

Python provides the [Signal](http://docs.python.org/library/signal.html) library allowing developers to catch Unix signals and set handlers for asynchronous events. For example, the `SIGTERM` \(Terminate\) signal is received when issuing a `kill` command for a given Unix process. Via the signal library, we can set a handler \(function\) callback that will be executed when that signal is received. Some signals however can not be handled/caught, such as the `SIGKILL` signal \(i.e. `kill -9`\). Please refer to the [Signal](http://docs.python.org/library/signal.html) library documentation for a full understanding of its use and capabilities.

A caveat when setting a signal handler is that only one handler can be defined for a given signal. Therefore, all handling must be done from a single callback function. This is a slight roadblock for applications built on Cement in that many pieces of the framework are broken out into independent extensions as well as applications that have 3rd party plugins. The trouble happens when the application, plugins, and framework extensions all need to perform some action when a signal is caught. This section outlines the recommended way of handling signals with Cement versus manually setting signal handlers that may collide.

{% hint style="warning" %}
It is important to note that it is not necessary to use the Cement mechanisms for signal handling, what-so-ever. That said, the primary concern of the framework is that `app.close()` is called no matter what the situation so that the `pre_close` and `post_close` framework hooks get run for cleanup.

Therefore, if you decide to disable signal handling all together you **must** ensure that you at the very least catch `signal.SIGTERM` and `signal.SIGINT` with the ability to call `app.close()` \(or allow the `with` operator to exit properly\).

You will likely find that it is more complex than you might think. The reason we put these mechanisms in place is primarily that we found it was the best way to a\) handle a signal, and b\) have access to our `app` object in order to be able to call `app.close()` when a process is terminated.
{% endhint %}

## Signals Caught by Default

By default Cement catches the signals `SIGTERM`, `SIGINT`, and `SIGHUP`. When these signals are caught, Cement raises the exception `CaughtSignal(signum, frame)` where `signum` and `frame` are the parameters passed to the signal handler. By raising an exception, we are able to pass runtime back to our applications main process \(within a try/except block\) and maintain the ability to access our application object without using global objects.

A basic application using default handling might look like:

{% tabs %}
{% tab title="Example: Default Signal Handling" %}
```python
import signal
from cement import App, CaughtSignal

with App('myapp') as app:
    try:
        app.run()
    except CaughtSignal as e:
        # do something with e.signum or e.frame
        if e.signum == signal.SIGTERM:
            app.log.warning('Caught SIGTERM')
        elif e.signum == signal.SIGINT:
            app.log.warning('Caught SIGINT')
```
{% endtab %}
{% endtabs %}

The above provides a very simple means of handling the most common signals, which in turn allows our application to "exit clean" by running `app.close()` and any `pre_close` or `post_close` hooks \(via `__exit__` from the `with` operator\).

{% hint style="warning" %}
If we don't catch the signals, then the exceptions will be unhandled and the application will not exit clean.
{% endhint %}

## Using the Signal Hook

An alternative way of adding multiple callbacks to a signal handler is by using the Cement `signal` hook. This hook is called anytime a handled signal is encountered.

{% tabs %}
{% tab title="Example: Using the Signal Hook" %}
{% code-tabs %}
{% code-tabs-item title="myapp.py" %}
```python
import signal
from cement import App, CaughtSignal

def my_signal_handler(app, signum, frame):
    # do something with app
    app.log.warning('Inside my_signal_handler')

    # do something with signum, or frame
    sig_name = signal.Signals(signum)
    print('Caught Signal %s' % sig_name)

class MyApp(App):
    class Meta:
        label = 'myapp'
        hooks = [
            ('signal', my_signal_handler),
        ]

with MyApp() as app:
    try:
        app.run()
    except CaughtSignal as e:
        # do something with e.signum, e.frame
        pass
```
{% endcode-tabs-item %}
{% endcode-tabs %}

Alternatively for extensions and plugins:

```python
def my_signal_handler(app, signum, frame):
    # do something with app
    app.log.warning('Inside my_signal_handler')

    # do something with signum, or frame
    sig_name = signal.Signals(signum)
    print('Caught Signal %s' % sig_name)

def load(app):
    app.hook.register('signal', my_signal_handler)
```
{% endtab %}
{% endtabs %}

The key thing to note here is that the main application itself can easily handle the `CaughtSignal` exception without using hooks. However, using the `signal` hook is useful for plugins and extensions to be able to tie into the signal handling outside of the main application. Both serve the same purpose.

Regardless of how signals are handled, all extensions or plugins should use the `pre_close` hook for cleanup purposes as much as possible as it is always run when `app.close()` is called.

## Configuring Which Signals To Catch

You can define what signals to catch via [App.Meta.catch\_signals](https://cement.readthedocs.io/en/3.0/api/core/foundation/#cement.core.foundation.App.Meta.catch_signals).

{% tabs %}
{% tab title="Example: Configuring Which Signals to Catch" %}
```python
import signal
from cement import App

class MyApp(App):
    class Meta:
        label = 'myapp'
        catch_signals = [
            signal.SIGTERM,
            signal.SIGINT,
            signal.SIGHUP,
        ]
```
{% endtab %}
{% endtabs %}

What happens is, Cement iterates over the `App.Meta.catch_signals` list and adds a generic handler function \(the same\) for each signal. Because the handler calls the cement `signal` hook, and then raises an exception which both pass the `signum` and `frame` parameters, you are able to handle the logic elsewhere rather than assigning a unique callback function for every signal.

## What If I Don't Like Your Signal Handler Callback?

If you want more control over what happens when a signal is caught, you are more than welcome to override the default signal handler callback. That said, please be kind and be sure to at least run the cement `signal` hook within your callback.

The following is an example taken from the builtin [`cement_signal_handler`](https://cement.readthedocs.io/en/3.0/api/core/foundation/#cement.core.foundation.cement_signal_handler) callback. Note that there is a bit of hackery in how we are acquiring the `CementApp` from the frame. This is because the signal is picked up outside of our control so we need to find it.

{% tabs %}
{% tab title="Example: Overriding the Builtin Signal Handler Callback" %}
```python
from cement import App

def my_signal_handler(signum, frame):
    """
    Catch a signal, run the ``signal`` hook, and then raise an exception
    allowing the app to handle logic elsewhere.

    Args:
        signum (int): The signal number
        frame: The signal frame

    Raises:
        cement.core.exc.CaughtSignal: Raised, passing ``signum``, and ``frame``

    """
    LOG.debug('Caught signal %s' % signum)

    for f_global in frame.f_globals.values():
        if isinstance(f_global, App):
            app = f_global
            for res in app.hook.run('signal', app, signum, frame):
                pass  # pragma: nocover

    raise exc.CaughtSignal(signum, frame)

class MyApp(App):
    class Meta:
        label = 'myapp'
        signal_handler = my_signal_handler
```
{% endtab %}
{% endtabs %}

## This Is Stupid, and UnPythonic - How Do I Disable It?

To each their own. If you simply do not want any kind of signal handling performed, just set `App.Meta.catch_signals = None`.

