r"""Documents
=============
"""
import json
import os
from typing import Any, Literal

from . import FILETYPE


def get_schema(
    filetype: FILETYPE,
) -> dict[str, Any]:
    r"""Get schema.

    :param filetype:
    :type filetype: Literal["build.sh", "subpackage.sh"]
    :rtype: dict[str, Any]
    """
    file = os.path.join(
        os.path.join(
            os.path.join(os.path.dirname(__file__), "assets"),
            "json",
        ),
        f"{filetype}.json",
    )
    with open(file, "r") as f:
        document = json.load(f)
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
