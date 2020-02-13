# Daemon

## Introduction

The Daemon Extension enables applications to easily perform standard daemonization operations.

**Features**

* Configurable runtime user and group
* Adds the `--daemon` command line option
* Add `app.daemonize()` function to trigger daemon functionality where necessary \(either in a cement `pre_run` hook or an application controller sub-command, etc\)
* Manages a PID file including cleanup on `app.close()`

**API References:**

* [Cement Daemon Extension](https://cement.readthedocs.io/en/3.0/api/ext/ext_daemon/)

## Requirements

* Python 2.6+, 3+

## Platform Support

* Unix/Linux
* macOS

## Configuration

The daemon extension is configurable with the following settings under a `[daemon]` section in the application configuration:

| Setting | **Description** |
| :--- | :--- |
| **user** | The user name the process runs as.  Default: `os.getlogin()` |
| **group** | The group name the process runs as. Default: _the primary group of the user_ |
| **dir** | The directory that the process runs in.  Default: `/` |
| **pid\_file** | The filesystem path to store the PID \(Process ID\) file.  Default: `None` |
| **umask** | The UMASK value to pass to `os.umask()`.  Default: `0` |

Configurations can be passed as defaults to `App`:

```python
from cement import App, init_defaults

DEFAULTS = init_defaults('myapp', 'daemon')
DEFAULTS['daemon']['user'] = 'myuser'
DEFAULTS['daemon']['group'] = 'mygroup'
DEFAULTS['daemon']['dir'] = '/var/lib/myapp/'
DEFAULTS['daemon']['pid_file'] = '/var/run/myapp/myapp.pid'
DEFAULTS['daemon']['umask'] = 0

class MyApp(App):
    class Meta:
        label = 'myapp'
        config_defaults = DEFAULTS
```

Application defaults are then overridden by configurations parsed via a `[demon]` config section in any of the applications configuration paths. An example configuration block would look like:

```text
[daemon]
user = myuser
group = mygroup
dir = /var/lib/myapp/
pid_file = /var/run/myapp/myapp.pid
umask = 0
```

## Usage

The following example shows how to add the daemon extension, as well as trigger daemon functionality before `app.run()` is called.

```python
from time import sleep
from cement import App

class MyApp(App):
    class Meta:
        label = 'myapp'
        extensions = ['daemon']

with MyApp() as app:
    app.daemonize()
    app.run()

    count = 0
    while True:
        count = count + 1
        print('Iteration: %s' % count)
        sleep(10)
```

Some applications may prefer to only daemonize certain sub-commands rather than the entire parent application. For example:

```python
from cement import App, Controller, ex

class Base(Controller):
    class Meta:
        label = 'base'

    @ex(help="run the daemon command.")
    def run_forever(self):
        from time import sleep
        self.app.daemonize()

        count = 0
        while True:
            count = count + 1
            print(count)
            sleep(10)

class MyApp(App):
    class Meta:
        label = 'myapp'
        handlers = [Base]
        extensions = ['daemon']

with MyApp() as app:
    app.run()
```

{% hint style="warning" %}
By default, even after `app.daemonize()` is called… the application will continue to run in the foreground, but will still manage the pid and user/group switching. To detach a process and send it to the background you simply pass the `--daemon` option at command line.
{% endhint %}

```text
$ python example.py --daemon

$ ps -x | grep example
37421 ??         0:00.01 python example2.py --daemon
37452 ttys000    0:00.00 grep example
```

### Daemonizing Without Commandline Option

Some use cases might require daemonizing the process without having to always pass the `--daemon` option, or where passing the option might be redundant. You can work around that programatically by simply overriding the `daemon` argument value in order to force daemonization even if `--daemon` wasn’t passed.

```python
app.pargs.daemon = True
app.daemonize()
```

Note that this would only work **after** arguments have been parsed \(i.e. after `app.run()` is called\).

