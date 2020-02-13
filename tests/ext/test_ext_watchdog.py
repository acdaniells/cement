import os
import time

from unittest.mock import Mock

from cement.core.exc import FrameworkError
from cement.ext.ext_watchdog import WatchdogEventHandler
from cement.utils import fs
from cement.utils.test import TestApp, raises


class MyEventHandler(WatchdogEventHandler):
    def on_any_event(self, event):
        # do something with the ``event`` object
        raise Exception("The modified path was: %s" % event.src_path)


class WatchdogApp(TestApp):
    class Meta:
        extensions = ["watchdog"]


def test_watchdog(tmp):
    # The exception is getting raised, but for some reason it's not being
    # caught by a with raises() block, so I'm mocking it out instead.
    MyEventHandler.on_any_event = Mock()
    with WatchdogApp() as app:
        app.watchdog.add(tmp.dir, event_handler=MyEventHandler)
        app.run()

        file_path = fs.join(tmp.dir, "test.file")
        # trigger an event
        f = open(file_path, "w")
        f.write("test data")
        f.close()
        time.sleep(1)

    # 3 separate calls:
    # File created
    # Dir modified
    # File modified
    assert MyEventHandler.on_any_event.call_count == 3


def test_watchdog_app_paths(tmp):
    class MyApp(WatchdogApp):
        class Meta:
            watchdog_paths = [(tmp.dir), (tmp.dir, WatchdogEventHandler)]

    WatchdogEventHandler.on_any_event = Mock()
    with MyApp() as app:
        app.run()

        WatchdogEventHandler.on_any_event.reset_mock()
        # trigger an event
        f = open(fs.join(tmp.dir, "test.file"), "w")
        f.write("test data")
        f.close()
        time.sleep(1)

    # 3 separate calls, called twice each because tmp.dir appears
    # twice in the watchdog_paths list
    # File created
    # Dir modified
    # File modified
    assert WatchdogEventHandler.on_any_event.call_count == 6


def test_watchdog_app_paths_bad_spec(tmp):
    class MyApp(WatchdogApp):
        class Meta:
            watchdog_paths = [[tmp.dir, WatchdogEventHandler]]

    with raises(FrameworkError, match="Watchdog path spec must be a tuple"):
        with MyApp():
            pass


def test_watchdog_default_event_handler(tmp):
    WatchdogEventHandler.on_any_event = Mock()
    with WatchdogApp() as app:
        app.watchdog.add(tmp.dir)
        app.run()

        f = open(fs.join(tmp.dir, "test.file"), "w")
        f.write("test data")
        f.close()
        time.sleep(1)
        # 3 separate calls:
        # File created
        # Dir modified
        # File modified
        assert WatchdogEventHandler.on_any_event.call_count == 3


def test_watchdog_bad_path(tmp):
    with WatchdogApp() as app:
        retval = app.watchdog.add(os.path.join(tmp.dir, "bogus_sub_dir"))
        app.run()
        assert not retval


def test_watchdog_hooks(tmp):
    # FIX ME: this is only coverage...
    def test_hook(app):
        app.counter += 1

    with WatchdogApp() as app:
        app.counter = 0
        app.watchdog.add(tmp.dir)
        app.hook.register("watchdog_pre_start", test_hook)
        app.hook.register("watchdog_post_start", test_hook)
        app.hook.register("watchdog_pre_stop", test_hook)
        app.hook.register("watchdog_post_stop", test_hook)
        app.hook.register("watchdog_pre_join", test_hook)
        app.hook.register("watchdog_post_join", test_hook)
        app.run()

    # yup, the function was run 6 times (once for each hook)
    assert app.counter == 6
