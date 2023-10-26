r"""Packages
============
"""
from .. import FILETYPE


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


def search_package_names(filetype: FILETYPE) -> list[str]:
    r"""Search package names.

    :param filetype:
    :type filetype: FILETYPE
    :rtype: list[str]
    """
    if filetype == "PKGBUILD":
        from .pkgbuild import get_package_names
    else:
        raise NotImplementedError
    return get_package_names()
