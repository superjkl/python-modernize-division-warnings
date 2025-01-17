from __future__ import generator_stop

from fissix import fixer_base, pytree
from fissix.pgen2 import token

from .. import utils


class FixImportDivisionFuture(fixer_base.BaseFix):
    PATTERN = """
    '/=' | '/'
    """

    def start_tree(self, tree, name):
        super().start_tree(tree, name)
        self.skip = "division" in tree.future_features

    def match(self, node):
        return node.value in ("/", "/=")

    def transform(self, node, results):
        if self.skip:
            return
        utils.add_future(node, "division")

