"""
Cement platform extension.
"""

import os
import platform
import socket

from cement.core.platform import PlatformHandler
from cement.utils.misc import minimal_logger

LOG = minimal_logger(__name__)


class CementPlatformHandler(PlatformHandler):

    """Cement platform handler implementation."""

    class Meta:

        """
        Handler meta-data (can be passed as keyword arguments to the parent
        class).
        """

        #: The string identifier of the handler.
        label = "cement"

    def __init__(self, **kw):
        super().__init__(**kw)
        self._platform = platform.platform()
        self._host = socket.gethostname()
        self._pid = os.getpid()

    @property
    def platform(self):
        """Returns the underlying platform."""
        return self._platform

    @property
    def host(self):
        """Returns the current hostname."""
        return self._host

    @property
    def pid(self):
        """Returns the current process identifier."""
        return self._pid


def load(app):
    app.handler.register(CementPlatformHandler)
