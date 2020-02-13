"""
Cement core platform module.
"""

from abc import abstractmethod

from cement.core.handler import Handler
from cement.core.interface import Interface
from cement.utils.misc import minimal_logger

LOG = minimal_logger(__name__)


class PlatformInterface(Interface):

    """
    This class defines the Platform Interface. Handlers that implement this
    interface must provide the methods and attributes defined below. In
    general, most implementations should sub-class from the provided
    :class:`PlatformHandler` base class as a starting point.
    """

    class Meta:

        """Handler meta-data."""

        #: The string identifier of the interface
        interface = "platform"

    @property
    @abstractmethod
    def platform(self):
        pass  # pragma: nocover

    @property
    @abstractmethod
    def host(self):
        pass  # pragma: nocover

    @property
    @abstractmethod
    def pid(self):
        pass  # pragma: nocover


class PlatformHandler(PlatformInterface, Handler):

    """Platform handler implementation."""

    pass  # pragma: nocover
