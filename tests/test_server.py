import os

from termux_language_server.server import TermuxLanguageServer as Server

server = Server("")
file = os.path.join(os.path.dirname(__file__), "PKGBUILD")
# namcap can't read it: its parser runs the package functions in a restricted
# shell, where cd fails and exits
unparsable = os.path.join(os.path.dirname(__file__), "unparsable", "PKGBUILD")


class Test:
    @staticmethod
    def test_check() -> None:
        diagnostics = server.lint(file)[file]
        assert len(diagnostics)

    @staticmethod
    def test_check_unparsable() -> None:
        diagnostics = server.lint(unparsable)[unparsable]
        assert any(
            diagnostic.message == "namcap couldn't read the PKGBUILD"
            for diagnostic in diagnostics
        )
