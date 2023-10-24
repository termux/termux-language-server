r"""Test documents"""
from termux_language_server.documents import get_schema


class Test:
    r"""Test."""

    @staticmethod
    def test_get_document() -> None:
        r"""Test get document.

        :rtype: None
        """
        assert len(
            get_schema("build.sh")
            .get("properties", {})
            .get("TERMUX_PKG_VERSION", {})
            .get("description", "")
            .splitlines()
        )
