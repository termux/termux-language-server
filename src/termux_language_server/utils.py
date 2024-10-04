r"""Utils
=========
"""

import json
import os
from typing import Any, Literal

from tree_sitter import Language, Parser, Query
from tree_sitter_bash import language as get_language_ptr

from . import FILETYPE

SCHEMAS = {}
QUERIES = {}
parser = Parser()
parser.language = Language(get_language_ptr())


def get_query(name: str, filetype: str = "bash") -> Query:
    r"""Get query.

    :param name:
    :type name: str
    :param filetype:
    :type filetype: str
    :rtype: Query
    """
    if name not in QUERIES:
        with open(
            os.path.join(
                os.path.dirname(__file__),
                "assets",
                "queries",
                f"{name}{os.path.extsep}scm",
            )
        ) as f:
            text = f.read()
        QUERIES[name] = parser.language.query(text)
    return QUERIES[name]


def get_schema(filetype: FILETYPE) -> dict[str, Any]:
    r"""Get schema.

    :param filetype:
    :type filetype: FILETYPE
    :rtype: dict[str, Any]
    """
    if filetype not in SCHEMAS:
        file = os.path.join(
            os.path.dirname(__file__),
            "assets",
            "json",
            f"{filetype}.json",
        )
        with open(file) as f:
            SCHEMAS[filetype] = json.load(f)
    return SCHEMAS[filetype]


def get_filetype(uri: str) -> FILETYPE | Literal[""]:
    r"""Get filetype.

    :param uri:
    :type uri: str
    :rtype: FILETYPE | Literal[""]
    """
    dirname = os.path.basename(os.path.dirname(uri))
    basename = os.path.basename(uri)
    ext = uri.split(os.path.extsep)[-1]
    if basename == "build.sh" and dirname != "scripts":
        return "build.sh"
    if basename.endswith(".subpackage.sh"):
        return "subpackage.sh"
    if ext == "install":
        return "install"
    if basename == "PKGBUILD":
        return "PKGBUILD"
    if basename == "makepkg.conf":
        return "makepkg.conf"
    if ext in {"ebuild", "eclass"}:
        return "ebuild"
    if basename == "make.conf":
        return "make.conf"
    if basename == "color.map":
        return "color.map"
    if ext == "mdd":
        return "mdd"
    if basename in {"devscripts.conf", ".devscripts"}:
        return "devscripts.conf"
    return ""
