from jinja2 import environmentfilter, nodes, TemplateError
from jinja2.ext import Extension
from markdown.extensions import toc
from markupsafe import Markup


@environmentfilter
def markdown(env, value):
    """
    Markdown filter with support for extensions.
    """
    try:
        import markdown as md
    except ImportError:
        raise TemplateError("Cannot load the markdown library")
    output = value

    extensions = ['admonition',
                  'meta',
                  'attr_list',
                  toc.TocExtension(baselevel=1, permalink=True),
                  'def_list',
                  'fenced_code',
                  'tables',
                  'sane_lists',
                  'codehilite',
                  'qualitas.ext.materialize_checklist',
                  'qualitas.ext.materialize_ul'
                  ]

    d = dict()
    d['extensions'] = list()
    d['extensions'].extend(extensions)

    marked = md.Markdown(**d)

    converted = marked.convert(output)

    return Markup(converted)


class Markdown(Extension):
    """
    A wrapper around the markdown filter for syntactic sugar.
    """
    tags = set(['markdown'])

    def parse(self, parser):
        """
        Parses the statements and defers to the callback
        for markdown processing.
        """
        lineno = next(parser.stream).lineno
        body = parser.parse_statements(['name:endmarkdown'], drop_needle=True)

        return nodes.CallBlock(
            self.call_method('_render_markdown'),
            [], [], body).set_lineno(lineno)

    def _render_markdown(self, caller=None):
        """
        Calls the markdown filter to transform the output.
        """
        if not caller:
            return ''
        output = caller().strip()
        return markdown(self.environment, output)
