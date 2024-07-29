r"""Provide ``__version__`` for
`importlib.metadata.version() <https://docs.python.org/3/library/importlib.metadata.html#distribution-versions>`_.
"""

from typing import Literal

try:
    from ._version import __version__, __version_tuple__  # type: ignore
except ImportError:  # for setuptools-generate
    __version__ = "rolling"
    __version_tuple__ = (0, 0, 0, __version__, "")

__all__ = ["__version__", "__version_tuple__"]

FILETYPE = Literal[
    "build.sh",
    "subpackage.sh",
    "PKGBUILD",
    "makepkg.conf",
    "install",
    "ebuild",
    "make.conf",
    "color.map",
    "mdd",
    "devscripts.conf",
]
PACKAGE_NAME = r"[a-z][a-z0-9-]*"
CSV = f"{PACKAGE_NAME}(, {PACKAGE_NAME})*"
