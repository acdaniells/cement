# Watchdog

## Introduction

The Watchdog Extension includes the [`WatchdogManager`](https://cement.readthedocs.io/en/3.0/api/ext/ext_watchdog/#cement.ext.ext_watchdog.WatchdogManager), enabling applications to easily monitor, and react to, changes in filesystem paths based on the filesystem events monitoring library [Watchdog](https://pypi.python.org/pypi/watchdog).

On application startup, the Watchdog Observer is automatically started and then upon application close, the observer thread is properly stopped and joined with the parent process before exit.

**API References:**

* [Cement Watchdog Extension](https://cement.readthedocs.io/en/3.0/api/ext/ext_watchdog/)
* [Watchdog Library](https://pythonhosted.org/watchdog/)

## Requirements

* Watchdog \(`pip install watchdog`\)

## Platform Support

* Unix/Linux
* macOS
* Windows

## Configuration

### Application Configuration Settings

This extension does not support any application level configuration settings.

### Application Meta Options

This extension honors the following application meta options:

| Option | **Description** |
| :--- | :--- |
| **watchdog\_paths** | A list of tuples that are passed directly as arguments to [`WatchdogManager.add()`](https://cement.readthedocs.io/en/3.0/api/ext/ext_watchdog/#cement.ext.ext_watchdog.WatchdogManager.add) \(a shortcut equivalent to `app.watchdog.add()`. |

## Hooks

This extension defines the following hooks:

### watchdog\_pre\_start

Run first when `App.watchdog.start()` is called. The application object is passed as an argument. Nothing is expected in return.

### watchdog\_post\_start

Run last when `App.watchdog.start()` is called. The application object is passed as an argument. Nothing is expected in return.

### watchdog\_pre\_stop

Run first when `App.watchdog.stop()` is called. The application object is passed as an argument. Nothing is expected in return.

### watchdog\_post\_stop

Run last when `App.watchdog.stop()` is called. The application object is passed as an argument. Nothing is expected in return.

### watchdog\_pre\_join

Run first when `App.watchdog.join()` is called. The application object is passed as an argument. Nothing is expected in return.

### watchdog\_post\_join

Run last when `App.watchdog.join()` is called. The application object is passed as an argument. Nothing is expected in return.

## Usage

The following example uses the default `WatchdogEventHandler` that by default only logs all events to `debug`:

{% tabs %}
{% tab title="Example: Using Watchdog Extension" %}
```python
from time import sleep
from cement import App, CaughtSignal
from cement.ext.ext_watchdog import WatchdogEventHandler

class MyApp(App):
    class Meta:
        label = 'myapp'
        extensions = ['watchdog']
        watchdog_paths = [
            ('./tmp/', WatchdogEventHandler),
        ]

with MyApp() as app:
    app.run()
    try:
        while True:
            sleep(1)
    except CaughtSignal as e:
        print(e)
```
{% endtab %}
{% endtabs %}

In the above example, nothing is printed to console. However you will see something like the following via debug logging:

```text
$ python myapp.py --debug 2>&1 | grep -i watchdog
cement.core.extension : loading the 'cement.ext.ext_watchdog' framework extension
cement.core.hook : defining hook 'watchdog_pre_start'
cement.core.hook : defining hook 'watchdog_post_start'
cement.core.hook : defining hook 'watchdog_pre_stop'
cement.core.hook : defining hook 'watchdog_post_stop'
cement.core.hook : defining hook 'watchdog_pre_join'
cement.core.hook : defining hook 'watchdog_post_join'
cement.core.hook : registering hook 'watchdog_extend_app' from cement.ext.ext_watchdog into hooks['post_setup']
cement.core.hook : registering hook 'watchdog_add_paths' from cement.ext.ext_watchdog into hooks['post_setup']
cement.core.hook : registering hook 'watchdog_start' from cement.ext.ext_watchdog into hooks['pre_run']
cement.core.hook : registering hook 'watchdog_cleanup' from cement.ext.ext_watchdog into hooks['pre_close']
cement.core.hook : running hook 'post_setup' (<function watchdog_extend_app at 0x103c991e0>) from cement.ext.ext_watchdog
cement.core.foundation : extending appication with '.watchdog' (<cement.ext.ext_watchdog.WatchdogManager object at 0x103f83ef0>)
cement.core.hook : running hook 'post_setup' (<function watchdog_add_paths at 0x103ddd6a8>) from cement.ext.ext_watchdog
cement.ext.ext_watchdog : adding path /path/to/tmp with event handler <class 'cement.ext.ext_watchdog.WatchdogEventHandler'>
cement.core.hook : running hook 'pre_run' (<function watchdog_start at 0x103ddd598>) from cement.ext.ext_watchdog
cement.ext.ext_watchdog : starting watchdog observer
myapp : Watchdog Event: <FileDeletedEvent: src_path='/path/to/tmp/test2'>
myapp : Watchdog Event: <FileDeletedEvent: src_path='/path/to/tmp/test4'>
myapp : Watchdog Event: <FileDeletedEvent: src_path='/path/to/tmp/test3'>
myapp : Watchdog Event: <FileDeletedEvent: src_path='/path/to/tmp/dir1/test'>
myapp : Watchdog Event: <FileDeletedEvent: src_path='/path/to/tmp/test'>
myapp : Watchdog Event: <DirDeletedEvent: src_path='/path/to/tmp/dir1'>
myapp : Watchdog Event: <DirModifiedEvent: src_path='/path/to/tmp'>
myapp : Watchdog Event: <DirModifiedEvent: src_path='/path/to/tmp'>
myapp : Watchdog Event: <DirCreatedEvent: src_path='/path/to/tmp/dir1'>
myapp : Watchdog Event: <FileCreatedEvent: src_path='/path/to/tmp/dir1/test.file'>
myapp : Watchdog Event: <DirModifiedEvent: src_path='/path/to/tmp/dir1'>
cement.core.hook : running hook 'pre_close' (<function watchdog_cleanup at 0x10e930620>) from cement.ext.ext_watchdog
cement.ext.ext_watchdog : stopping watchdog observer
cement.ext.ext_watchdog : joining watchdog observer
cement.core.foundation : closing the myapp application
```

To expand on the above example, we can add our own event handlers:

{% tabs %}
{% tab title="Example: Adding Watchdog Event Handlers" %}
{% code-tabs %}
{% code-tabs-item title="myapp.py" %}
```python
from time import sleep
from cement import App, CaughtSignal
from cement.ext.ext_watchdog import WatchdogEventHandler

class MyEventHandler(WatchdogEventHandler):
    def on_any_event(self, event):
        # do something with the ``event`` object
        print("The modified path was: %s" % event.src_path)

class MyApp(App):
    class Meta:
        label = 'myapp'
        extensions = ['watchdog']
        watchdog_paths = [
            ('./tmp/', MyEventHandler),
        ]

with MyApp() as app:
    app.run()

    try:
        while True:
            sleep(1)
    except CaughtSignal as e:
        print(e)
```
{% endcode-tabs-item %}
{% endcode-tabs %}
{% endtab %}

{% tab title="cli" %}
```text
$ python myapp.py
The modified path was: /path/to/tmp/test.file
```
{% endtab %}
{% endtabs %}

{% hint style="info" %}
Note that the `WatchdogEventHandler` could be replaced with any other event handler classe \(i.e. those available from `watchdog` directly\). However to play nicely with Cement, we sub-class them first in order to pass in our application object.
{% endhint %}

{% tabs %}
{% tab title="Example: Creating a Watchdog Event Handler" %}
```python
from watchdog.events import FileSystemEventHandler

class MyEventHandler(FileSystemEventHandler):
    def __init__(self, app, *args, **kw):
        super(MyEventHandler, self).__init__(*args, **kw)
        self.app = app
```
{% endtab %}
{% endtabs %}

For full usage of Watchdog event handlers, refer to the [Watchdog API Documentation](http://pythonhosted.org/watchdog/index.html).

