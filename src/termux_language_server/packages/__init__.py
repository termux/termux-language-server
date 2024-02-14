r"""Packages
============
"""

from .. import FILETYPE

PACKAGE_VARIABLES = {
    "PKGBUILD": {
        "depends",
        "makedepends",
        "optdepends",
        "conflicts",
        "provides",
        "replaces",
    }
}


def search_package_document(name: str, filetype: FILETYPE) -> str:
    r"""Search package document.

    :param name:
    :type name: str
    :param filetype:
    :type filetype: FILETYPE
    :rtype: str
    """
    if filetype == "PKGBUILD":
        from .pkgbuild import get_package_document
    else:
        raise NotImplementedError
    return get_package_document(name)


def search_package_names(name: str, filetype: FILETYPE) -> dict[str, str]:
    r"""Search package names.

    :param name:
    :type name: str
    :param filetype:
    :type filetype: FILETYPE
    :rtype: dict[str, str]
    """
    if filetype == "PKGBUILD":
        from .pkgbuild import get_package_names
    else:
        raise NotImplementedError
    return get_package_names(name)
