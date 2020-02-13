"""
Cement tabulate extension module.
"""

from cement.core import output
from cement.utils.misc import minimal_logger

from tabulate import tabulate

LOG = minimal_logger(__name__)


class TabulateOutputHandler(output.OutputHandler):

    """
    This class implements the :ref:`Output <cement.core.output>` Handler
    interface. It provides tabulated text output using the
    `Tabulate <https://pypi.python.org/pypi/tabulate>`_ module. Please
    see the developer documentation on :cement:`Output Handling <dev/output>`.

    **Note** This extension has an external dependency on ``tabulate``. You
    must include ``tabulate`` in your applications dependencies as Cement
    explicitly does **not** include external dependencies for optional
    extensions.
    """

    class Meta:

        """Handler meta-data."""

        label = "tabulate"

        #: Default headers to use.
        headers = []

        #: Default template format. See the ``tabulate`` documentation for
        #: all supported template formats.
        format = "psql"

        #: String format to use for float values.
        float_format = "g"

        #: Default alignment for string columns. See the ``tabulate``
        #: documentation for all supported ``stralign`` options.
        string_alignment = "left"

        #: Default alignment for numeric columns. See the ``tabulate``
        #: documentation for all supported ``numalign`` options.
        numeric_alignment = "right"

        #: Default replacement for missing value.
        missing_value = ""

        #: Whether or not to show a row index column. See the ``tabulate``
        #: documentation for all supported ``showindex`` options.
        show_index = True

        #: Disable number parsing (and alignment). See the ``tabulate``
        #: documentation for all supported ``disable_numparse`` options.
        disable_numeric_parsing = False

        #: Whether or not to pad the output with an extra pre/post '\n'.
        padding = True

        #: Whether or not to include ``tabulate`` as an available to choice
        #: to override the ``output_handler`` via command line options.
        overridable = False

    def render(self, data, **kw):
        """
        Take a data dictionary and render it into a table. Additional
        keyword arguments are passed directly to ``tabulate.tabulate``.

        Args:
            data_dict (dict): The data dictionary to render.

        Returns:
            str: The rendered template text

        """
        headers = kw.get("headers", self._meta.headers)

        out = tabulate(
            data,
            headers,
            tablefmt=kw.get("tablefmt", self._meta.format),
            floatfmt=kw.get("floatfmt", self._meta.float_format),
            numalign=kw.get("numalign", self._meta.numeric_alignment),
            stralign=kw.get("stralign", self._meta.string_alignment),
            missingval=kw.get("missingval", self._meta.missing_value),
            showindex=kw.get("showindex", self._meta.show_index),
            disable_numparse=kw.get(
                "disable_numparse", self._meta.disable_numeric_parsing
            ),
        )
        out = out + "\n"

        if self._meta.padding is True:
            out = "\n" + out + "\n"

        return out


def load(app):
    app.handler.register(TabulateOutputHandler)
