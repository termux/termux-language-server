r"""Documents
=============
"""
import json
import os
from typing import Any, Literal

from platformdirs import user_cache_dir

from .. import FILETYPE


def get_schema(
    filetype: FILETYPE,
    method: Literal["builtin", "cache", "web"] = "builtin",
) -> dict[str, Any]:
    r"""Get schema. ``builtin`` will use builtin termux.json. ``cache``
    will generate a cache from
    `<https://github.com/termux/termux-packages/wiki/Creating-new-package>`_.
    ``web`` is same as ``cache`` except it doesn't generate cache. We use
    ``builtin`` as default.

    :param filetype:
    :type filetype: Literal["build.sh", "subpackage.sh"]
    :param method:
    :type method: Literal["builtin", "cache", "web"]
    :rtype: dict[str, Any]
    """
    if method == "builtin":
        file = os.path.join(
            os.path.join(
                os.path.join(
                    os.path.dirname(os.path.dirname(__file__)), "assets"
                ),
                "json",
            ),
            f"{filetype}.json",
        )
        with open(file, "r") as f:
            document = json.load(f)
    elif method == "cache":
        from .termux import init_schema

        if not os.path.exists(user_cache_dir(f"{filetype}.json")):
            document = init_schema()[filetype]
            with open(user_cache_dir(f"{filetype}.json"), "w") as f:
                json.dump(document, f, indent=2)
        else:
            with open(user_cache_dir(f"{filetype}.json"), "r") as f:
                document = json.load(f)
    else:
        from .termux import init_schema

        document = init_schema()[filetype]
    return document


def get_filetype(uri: str) -> Literal["build.sh", "subpackage.sh", ""]:
    r"""Get filetype.

    :param uri:
    :type uri: str
    :rtype: Literal["build.sh", "subpackage.sh", ""]
    """
    if os.path.basename(uri) == "build.sh":
        return "build.sh"
    if os.path.basename(uri).endswith(".subpackage.sh"):
        return "subpackage.sh"
    return ""
