"""
Cement core log module.
"""

from abc import abstractmethod

from cement.core.handler import Handler
from cement.core.interface import Interface


class LogInterface(Interface):

    """
    This class defines the Log Interface.  Handlers that implement this
    interface must provide the methods and attributes defined below. In
    general, most implementations should sub-class from the provided
    :class:`LogHandler` base class as a starting point.
    """

    class Meta:

        """Handler meta-data."""

        #: The string identifier of the interface.
        interface = "log"

    @abstractmethod
    def set_level(self):
        """
        Set the log level.  Must except atleast one of:
            ``['INFO', 'WARNING', 'ERROR', 'DEBUG', or 'CRITICAL']``.

        """
        pass  # pragma: nocover

    @abstractmethod
    def get_level(self):
        """Return a string representation of the log level."""
        pass  # pragma: nocover

    @abstractmethod
    def info(self, msg):
        """
        Log to the ``INFO`` facility.

        Args:
            msg (str): The message to log.

        """
        pass  # pragma: nocover

    @abstractmethod
    def warning(self, msg):
        """
        Log to the ``WARNING`` facility.

        Args:
            msg (str): The message to log.

        """
        pass  # pragma: nocover

    @abstractmethod
    def error(self, msg):
        """
        Log to the ``ERROR`` facility.

        Args:
            msg (str): The message to log.

        """
        pass  # pragma: nocover

    @abstractmethod
    def critical(self, msg):
        """
        Log to the ``CRITICAL`` facility.

        Args:
            msg (str): The message to log.

        """
        pass  # pragma: nocover

    @abstractmethod
    def debug(self, msg):
        """
        Log to the ``DEBUG`` facility.

        Args:
            msg (str): The message to log.

        """
        pass  # pragma: nocover


class LogHandler(LogInterface, Handler):

    """
    Log handler implementation.

    """

    pass  # pragma: nocover
