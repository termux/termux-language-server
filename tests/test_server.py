import os

from termux_language_server.server import TermuxLanguageServer as Server

server = Server("")
file = os.path.join(os.path.dirname(__file__), "PKGBUILD")


class Test:
    @staticmethod
    def test_check() -> None:
        diagnostics = server.lint(file)[file]
        assert len(diagnostics)
