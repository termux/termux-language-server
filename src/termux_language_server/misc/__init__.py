r"""Misc
========
"""

from typing import Any

from .. import FILETYPE


def get_schema(filetype: FILETYPE) -> dict[str, Any]:
    r"""Get schema.

    :param filetype:
    :type filetype: FILETYPE
    :rtype: dict[str, Any]
    """
    if filetype in {"build.sh", "subpackage.sh"}:
        from .termux import init_schema
    elif filetype in {"PKGBUILD", "install"}:
        from .pkgbuild import init_schema
    elif filetype == "makepkg.conf":
        from .makepkg_conf import init_schema
    elif filetype == "color.map":
        from .color_map import init_schema
    elif filetype == "make.conf":
        from .make_conf import init_schema
    elif filetype == "ebuild":
        from .ebuild import init_schema
    else:
        raise NotImplementedError(filetype)
    return init_schema()[filetype]
