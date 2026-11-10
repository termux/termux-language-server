import os

import pytest
from lsprotocol.types import DiagnosticSeverity

from termux_language_server.server import TermuxLanguageServer as Server

server = Server("")
file = os.path.join(os.path.dirname(__file__), "PKGBUILD")
unparsable = os.path.join(os.path.dirname(__file__), "unparsable", "PKGBUILD")


class Test:
    @staticmethod
    def test_check() -> None:
        diagnostics = server.lint(file)[file]
        assert len(diagnostics)

    @staticmethod
    def test_check_unparsable() -> None:
        pytest.importorskip("Namcap")
        diagnostics = server.lint(unparsable)[unparsable]
        assert any(
            diagnostic.severity == DiagnosticSeverity.Information
            for diagnostic in diagnostics
        )
