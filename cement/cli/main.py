#!/usr/bin/env python3

import os
import sys

from cement import App, CaughtSignal
from cement.cli.controllers.base import Base

sys.path.append(os.path.join(os.path.dirname(__file__), "contrib"))


class CementApp(App):
    """Cement developer application."""

    class Meta:
        label = "cement"
        controller = "base"
        template_module = "cement.cli.templates"
        template_handler = "jinja2"
        config_handler = "yaml"
        config_file_suffix = ".yml"

        extensions = ["generate", "yaml", "jinja2"]

        handlers = [Base]


class CementTestApp(CementApp):
    """Cement testing application."""

    class Meta:
        argv = []
        config_files = []
        exit_on_close = False


def main(argv=None):
    with CementApp() as app:
        try:
            app.run()
        except AssertionError as e:  # pragma: nocover
            print("AssertionError > %s" % e.args[0])  # pragma: nocover
            app.exit_code = 1  # pragma: nocover
        except CaughtSignal as e:  # pragma: nocover
            print("\n%s" % e)  # pragma: nocover
            app.exit_code = 0  # pragma: nocover


if __name__ == "__main__":
    main()  # pragma: nocover
