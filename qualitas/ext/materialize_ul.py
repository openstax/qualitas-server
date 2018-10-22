# https://github.com/Dogfalo/materialize/issues/2582

import re

from markdown.extensions import Extension
from markdown.postprocessors import Postprocessor


def makeExtension():
    return MaterializeListExtension()


class MaterializeListExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        postprocessor = MaterializeULPostprocessor(md)
        md.postprocessors.add('materializeul', postprocessor, '>raw_html')


class MaterializeULPostprocessor(Postprocessor):
    """
    Adds default-browser class to unordered lists
    """

    list_pattern = re.compile(r'(<ul>)')

    def run(self, html):
        return re.sub(self.list_pattern, self._convert_list, html)

    def _convert_list(self, match):
        return match.group(1).replace('<ul>',
                                      '<ul class="browser-default">')
