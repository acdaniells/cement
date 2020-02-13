"""
Cement colorlog extension module.
"""

import logging
import os
import sys

from cement.ext.ext_logging import LoggingLogHandler
from cement.utils.misc import is_true

from colorlog import ColoredFormatter


class ColorLogHandler(LoggingLogHandler):

    """
    This class implements the Log Handler interface.  It is
    a sub-class of :class:`cement.ext.ext_logging.LoggingLogHandler` which is
    based on the standard :py:class:`logging` library, and adds colorized
    console output using the
    `ColorLog <https://pypi.python.org/pypi/colorlog>`_ library.

    **Note** This extension has an external dependency on ``colorlog``.  You
    must include ``colorlog`` in your applications dependencies as Cement
    explicitly does **not** include external dependencies for optional
    extensions.

    """

    class Meta:

        """Handler meta-data."""

        #: The string identifier of the handler.
        label = "colorlog"

        #: Color mapping for each log level
        colors = {
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "blue",
            "ERROR": "red",
            "CRITICAL": "fg_bold_white,bg_red",
        }

        #: Secondary colors
        secondary_colors = {}

        #: Default configuration settings.  Will be overridden by the same
        #: settings in any application configuration file under a
        #: ``[log.colorlog]`` block.
        config_defaults = dict(
            file=None,
            level="INFO",
            to_console=True,
            rotate=False,
            max_bytes=512_000,
            max_files=4,
            colorize_file_log=False,
            colorize_console_log=True,
        )

        #: Formatter class to use for non-colorized logging (non-tty, file,
        #: etc)
        formatter_class_without_color = logging.Formatter

        #: Formatter class to use for colorized logging
        formatter_class = ColoredFormatter

    def _get_console_format(self):
        format = super()._get_console_format()
        colorize = self.app.config.get("log.colorlog", "colorize_console_log")
        if sys.stdout.isatty() or "CEMENT_TEST" in os.environ:
            if is_true(colorize):
                for key in self._meta.secondary_colors.keys():
                    format = format.replace(
                        f"{{{key}}}",
                        f"{{reset}}{{{key}_log_color}}{{{key}}}{{reset}}{{log_color}}",
                    )
                format = "{log_color}" + format
        return format

    def _get_file_format(self):
        format = super()._get_file_format()
        colorize = self.app.config.get("log.colorlog", "colorize_file_log")
        if is_true(colorize):
            for key in self._meta.secondary_colors.keys():
                format = format.replace(
                    f"{{{key}}}",
                    f"{{reset}}{{{key}_log_color}}{{{key}}}{{reset}}{{log_color}}",
                )
            format = "{log_color}" + format
        return format

    def _get_console_formatter(self, format):
        colorize = self.app.config.get("log.colorlog", "colorize_console_log")

        if sys.stdout.isatty() or "CEMENT_TEST" in os.environ:
            if is_true(colorize):
                formatter = self._meta.formatter_class(
                    format,
                    datefmt=self._meta.date_format,
                    style=self._meta.format_style,
                    log_colors=self._meta.colors,
                    secondary_log_colors=self._meta.secondary_colors,
                )
            else:
                formatter = self._meta.formatter_class_without_color(
                    format,
                    datefmt=self._meta.date_format,
                    style=self._meta.format_style,
                )
        else:
            klass = self._meta.formatter_class_without_color  # pragma: nocover
            formatter = klass(  # pragma: nocover
                format,
                datefmt=self._meta.date_format,
                style=self._meta.format_style,  # pragma: nocover
            )  # pragma: nocover

        return formatter

    def _get_file_formatter(self, format):
        colorize = self.app.config.get("log.colorlog", "colorize_file_log")

        if is_true(colorize):
            formatter = self._meta.formatter_class(
                format,
                datefmt=self._meta.date_format,
                style=self._meta.format_style,
                log_colors=self._meta.colors,
                secondary_log_colors=self._meta.secondary_colors,
            )
        else:
            formatter = self._meta.formatter_class_without_color(
                format, datefmt=self._meta.date_format, style=self._meta.format_style
            )

        return formatter


def load(app):
    app.handler.register(ColorLogHandler)
