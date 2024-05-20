r"""Test schema."""

import os

from lsp_tree_sitter.finders import SchemaFinder
from termux_language_server.schema import BashTrie
from termux_language_server.utils import get_filetype, get_schema, parser

PATH = os.path.dirname(__file__)


class Test:
    r"""Test."""

    @staticmethod
    def test_SchemaFinder() -> None:
        r"""Test schemafinder.

        :rtype: None
        """
        path = os.path.join(PATH, "build.sh")
        filetype = get_filetype(path)
        assert filetype == "build.sh"
        with open(path, "rb") as f:
            text = f.read()
        tree = parser.parse(text)
        finder = SchemaFinder(get_schema(filetype), BashTrie)
        diagnostics = finder.get_diagnostics(path, tree)
        assert len(diagnostics) > 0
