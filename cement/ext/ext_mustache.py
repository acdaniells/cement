"""
Cement mustache extension module.
"""

from cement.core.output import OutputHandler
from cement.core.template import TemplateHandler
from cement.utils.misc import minimal_logger

from pystache.renderer import Renderer

LOG = minimal_logger(__name__)


class PartialsLoader:
    def __init__(self, handler):
        self.handler = handler

    def get(self, template):
        content, _type, _path = self.handler.load(template)
        return content


class MustacheOutputHandler(OutputHandler):

    """
    This class implements the :ref:`Output <cement.core.output>` Handler
    interface.  It provides text output from template and uses the
    `Mustache Templating Language <http://mustache.github.com>`_.  Please
    see the developer documentation on
    :cement:`Output Handling <dev/output>`.

    **Note** This extension has an external dependency on ``pystache``.  You
    must include ``pystache`` in your applications dependencies as Cement
    explicitly does **not** include external dependencies for optional
    extensions.
    """

    class Meta:

        """Handler meta-data."""

        label = "mustache"

        #: Whether or not to include ``mustache`` as an available to choice
        #: to override the ``output_handler`` via command line options.
        overridable = False

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        # self._partials_loader = PartialsLoader(self)
        self.templater = None

    def _setup(self, app):
        super()._setup(app)
        self.templater = self.app.handler.resolve("template", "mustache", setup=True)

    def render(self, data, template=None, **kw):
        """
        Take a data dictionary and render it using the given template file.
        Additional keyword arguments passed to ``stache.render()``.

        Args:
            data (dict): The data dictionary to render.

        Keyword Args:
            template (str): The path to the template, after the
                ``template_module`` or ``template_dirs`` prefix as defined in
                the application.

        Returns:
            str: The rendered template text

        """

        LOG.debug("rendering content using '%s' as a template." % template)
        content, _type, _path = self.templater.load(template)
        return self.templater.render(content, data)


class MustacheTemplateHandler(TemplateHandler):

    """
    This class implements the :ref:`Template <cement.core.template>` Handler
    interface.  It renderd content as template, and supports copying entire
    source template directories using the
    `Mustache Templating Language <http://mustache.github.com>`_.  Please
    see the developer documentation on
    :cement:`Template Handling <dev/template>`.

    **Note** This extension has an external dependency on ``pystache``.  You
    must include ``pystache`` in your applications dependencies as Cement
    explicitly does **not** include external dependencies for optional
    extensions.
    """

    class Meta:

        """Handler meta-data."""

        label = "mustache"

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self._partials_loader = PartialsLoader(self)

    def render(self, content, data):
        """
        Render the given ``content`` as template with the ``data`` dictionary.

        Args:
            content (str): The template content to render.
            data (dict): The data dictionary to render.

        Returns:
            str: The rendered template text

        """

        stache = Renderer(partials=self._partials_loader)
        return stache.render(content, data)


def load(app):
    app.handler.register(MustacheOutputHandler)
    app.handler.register(MustacheTemplateHandler)
