r"""Test schema."""
import os

from termux_language_server.documents import get_filetype, get_schema
from termux_language_server.parser import parse
from termux_language_server.schema import BashTrie
from termux_language_server.tree_sitter_lsp.finders import SchemaFinder

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
        tree = parse(text)
        finder = SchemaFinder(get_schema(filetype), BashTrie)
        diagnostics = finder.get_diagnostics(path, tree)
        assert len(diagnostics) > 0
