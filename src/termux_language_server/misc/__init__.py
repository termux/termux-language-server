r"""Misc
========
"""
from typing import Any


def get_schema(filetype: str) -> dict[str, Any]:
    r"""Get schema.

    :param filetype:
    :type filetype: str
    :rtype: dict[str, Any]
    """
    if filetype in {"build.sh", "subpackage.sh"}:
        from .termux import init_schema
    elif filetype in {"PKGBUILD", "install"}:
        from .pkgbuild import init_schema
    elif filetype in {"color.map", "make.conf", "ebuild"}:
        from .portage import init_schema
    else:
        raise NotImplementedError(filetype)
    return init_schema()[filetype]
