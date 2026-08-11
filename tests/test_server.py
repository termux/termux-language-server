import os

from lsp_tree_sitter.linter import PackageLinter
from lsp_tree_sitter.node import NodeText

from termux_language_server.server import TermuxLanguageServer as Server

server = Server("")
file = os.path.join(os.path.dirname(__file__), "PKGBUILD")


class Test:
    @staticmethod
    def test_check() -> None:
        diagnostics = server.lint(file)[file]
        assert len(diagnostics)

    @staticmethod
    def test_expansion_fragments_are_not_captured() -> None:
        source = b"""pkgname=foo
pkgver=1.0
pkgrel=1
pkgdesc='repro'
arch=('any')
conflicts=("${pkgname%-bar}-bin" "${pkgname}-git")
provides=("${pkgname%-bar}=${pkgver}")
depends=('boost-libs' "rapidjson")
"""
        linter = next(
            item for item in server.linters if isinstance(item, PackageLinter)
        )
        tree = server.parser.parse(source)
        names = {
            str(NodeText(node))
            for node in linter.cursor.captures(tree.root_node).get(
                "package.PKGBUILD", []
            )
        }
        assert not {"-bin", "-git", "="} & names
        assert {"'boost-libs'", "rapidjson"} <= names
