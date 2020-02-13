# Alarm

## Introduction

The Alarm Extension provides the [AlarmManager](http://cement.readthedocs.io/en/3.0/api/ext/ext_alarm/#cement.ext.ext_alarm.AlarmManager) extended object, with easy mechanisms for handling long running operations that might timeout after a set amount of time.

**API References:**

* [Cement Alarm Extension](http://cement.readthedocs.io/en/3.0/api/ext/ext_alarm/)
* [Python Signal Library](https://docs.python.org/3.5/library/signal.html)

## **Requirements**

* No external dependencies

## Platform Support

* Unix
* Linux
* macOS \(Darwin\)

## **Configuration**

This extension does not rely on any application level configuration settings or meta options.

## **Usage**

{% tabs %}
{% tab title="Example: Using Alarm Extension" %}
```python
import time
from cement import App, CaughtSignal

class MyApp(App):
    class Meta:
        label = 'myapp'
        exit_on_close = True
        extensions = ['alarm']


with MyApp() as app:
    try:
        app.run()
        app.alarm.set(3, "The operation timed out after 3 seconds!")

        # do something that takes time to operate
        time.sleep(5)

        app.alarm.stop()

    except CaughtSignal as e:
        print(e.msg)
        app.exit_code = 1
```
{% endtab %}

{% tab title="cli" %}
```text
$ python myapp.py
ERROR: The operation timed out after 3 seconds!
Caught signal 14
```
{% endtab %}
{% endtabs %}

