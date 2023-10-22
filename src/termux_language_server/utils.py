r"""Utils
=========
"""
from typing import Callable, Literal

from tree_sitter import Tree

from .documents import get_document, get_filetype
from .finders import (
    InvalidNodeFinder,
    RequireNodesFinder,
    UnsortedNodesFinder,
    UnsortedPackageFinder,
)
from .tree_sitter_lsp.diagnose import check as _check
from .tree_sitter_lsp.finders import ErrorFinder, MissingFinder
from .tree_sitter_lsp.format import format as _format

DIAGNOSTICS_FINDERS = [
    ErrorFinder(),
    MissingFinder(),
]


def get_keywords(document: dict[str, tuple[str, str]]) -> dict[str, list[str]]:
    r"""Get keywords.

    :param document:
    :type document: dict[str, tuple[str, str]]
    :rtype: dict[str, list[str]]
    """
    keywords = {"build.sh": [], "subpackage.sh": []}
    for k, v in document.items():
        if v[1] == "build.sh":
            keywords["build.sh"] += [k]
        if v[1] == "subpackage.sh":
            keywords["subpackage.sh"] += [k]
    return keywords


def get_paths(paths: list[str]) -> dict[str, list[str]]:
    r"""Get paths.

    :param paths:
    :type paths: list[str]
    :rtype: dict[str, list[str]]
    """
    _paths = {"build.sh": [], "subpackage.sh": []}
    for path in paths:
        filetype = get_filetype(path)
        if filetype == "build.sh":
            _paths["build.sh"] += [path]
        elif filetype == "subpackage.sh":
            _paths["subpackage.sh"] += [path]
        else:
            raise NotImplementedError
    return _paths


def check(
    paths: list[str],
    parse: Callable[[bytes], Tree],
    color: Literal["auto", "always", "never"] = "auto",
) -> int:
    r"""Check.

    :param paths:
    :type paths: list[str]
    :param parse:
    :type parse: Callable[[bytes], Tree]
    :param color:
    :type color: Literal["auto", "always", "never"]
    :rtype: int
    """
    document, required, csvs = get_document()
    keywords = get_keywords(document)
    _paths = get_paths(paths)
    return sum(
        _check(
            _paths[filetype],
            DIAGNOSTICS_FINDERS
            + [
                RequireNodesFinder(required[filetype]),
                InvalidNodeFinder(set(keywords[filetype])),
                UnsortedNodesFinder(keywords[filetype]),
                UnsortedPackageFinder(csvs[filetype]),
            ],
            parse,
            color,
        )
        for filetype in ["build.sh", "subpackage.sh"]
    )


def format(
    paths: list[str],
    parse: Callable[[bytes], Tree],
) -> None:
    r"""Format.

    :param paths:
    :type paths: list[str]
    :param parse:
    :type parse: Callable[[bytes], Tree]
    :rtype: None
    """
    document, _, csvs = get_document()
    keywords = get_keywords(document)
    _paths = get_paths(paths)
    for filetype in ["build.sh", "subpackage.sh"]:
        _format(
            _paths[filetype],
            [
                UnsortedNodesFinder(keywords[filetype]),
                UnsortedPackageFinder(csvs[filetype]),
            ],
            parse,
        )
