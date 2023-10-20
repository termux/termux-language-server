r"""Test documents"""
from termux_language_server.documents import get_document


class Test:
    r"""Test."""

    @staticmethod
    def test_get_document() -> None:
        r"""Test get document.

        :rtype: None
        """
        assert len(get_document().get("TERMUX_PKG_NAME", "")[0].splitlines())
