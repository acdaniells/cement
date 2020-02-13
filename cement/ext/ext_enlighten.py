"""
Cement enlighten extension.
"""

from cement.core import exc, meta
from cement.utils.misc import minimal_logger

import enlighten

LOG = minimal_logger(__name__)


class EnlightenManager(meta.MetaMixin):

    """Enlighten progress bar manager class."""

    class Meta:
        """Manager meta-data."""

        #: Default progress bar format
        default_bar_format = (
            "{desc}{desc_pad}{percentage:3.0f}%|{bar}|"
            " {count:{len_total}d}/{total:d} [{elapsed}<{eta},"
            " {rate:.2f}{unit_pad}{unit}/s]"
        )

    def __init__(self, app, *args, **kw):
        super().__init__(*args, **kw)
        self.app = app
        self.__counters__ = {}
        self._manager = enlighten.get_manager()
        self.stopped = False

    def stop(self):
        """Stops the progress bar manager."""

        if self.stopped:
            return

        for name in self.__counters__.keys():
            self.update(name, incr=self._count_remainder(name))
            self.get(name).close()

        self.__counters__ = {}
        self._manager.stop()
        self.stopped = True
        print()  # clear a row on the console to stop less getting upset

        LOG.debug("Enlighten manager stopped")

    def add(self, name, **kw):
        """Adds a progress bar."""

        name = name.lower()

        if self.__counters__.get(name):
            raise exc.FrameworkError(
                f"{self._meta.object_name} '{name}' already exists"
            )

        bar_format = kw.get("bar_format", self._meta.default_bar_format)

        kw["bar_format"] = "  " * kw.get("indent", 0) + bar_format

        counter = self._manager.counter(**kw)

        self.__counters__[name] = counter

    def remove(self, name):
        """Removes a progress bar."""

        name = name.lower()
        self.update(name, incr=self._count_remainder(name))
        self.get(name).close()
        self.__counters__.pop(name)

    def get(self, name):
        """Returns a given progress bar object."""
        name = name.lower()
        counter = self.__counters__.get(name)

        if counter is None:
            raise exc.FrameworkError(f"Counter '{name}' does not exists")

        return counter

    def update(self, name, **kw):
        """Update a given progress bar."""

        name = name.lower()

        if kw.get("incr"):
            self.get(name).update(kw.get("incr"))

        if kw.get("desc"):
            self.get(name).desc = kw.get("desc")

        for counter in self.__counters__.values():
            counter.refresh()

    def _count_remainder(self, name):
        counter = self.get(name)

        return counter.total - counter.count


def enlighten_extend_app(app):
    app.extend("enlighten", EnlightenManager(app))


def enlighten_cleanup(app):
    app.enlighten.stop()


def load(app):
    app.hook.register("post_setup", enlighten_extend_app)
    app.hook.register("pre_close", enlighten_cleanup)
