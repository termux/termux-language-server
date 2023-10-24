r"""Utils
=========
"""
from typing import Callable, Literal

from tree_sitter import Tree

from . import FILETYPE
from .documents import get_filetype
from .finders import (
    InvalidKeywordFinder,
    RequiredKeywordFinder,
    UnsortedCSVFinder,
    UnsortedKeywordFinder,
)
from .tree_sitter_lsp.diagnose import check as _check
from .tree_sitter_lsp.finders import ErrorFinder, MissingFinder
from .tree_sitter_lsp.format import format as _format

DIAGNOSTICS_FINDERS = [
    ErrorFinder(),
    MissingFinder(),
]


def get_paths(paths: list[str]) -> dict[FILETYPE, list[str]]:
    r"""Get paths.

    :param paths:
    :type paths: list[str]
    :rtype: dict[FILETYPE, list[str]]
    """
    _paths = {k: [] for k in FILETYPE.__args__}  # type: ignore
    for path in paths:
        filetype = get_filetype(path)
        for _filetype, filepaths in _paths.items():
            if filetype == _filetype:
                filepaths += [path]
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
    return sum(
        _check(
            _paths,
            DIAGNOSTICS_FINDERS
            + [
                RequiredKeywordFinder(filetype),
                InvalidKeywordFinder(filetype),
                UnsortedKeywordFinder(filetype),
                UnsortedCSVFinder(filetype),
            ],
            parse,
            color,
        )
        for filetype, _paths in get_paths(paths).items()
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
    for filetype, _paths in get_paths(paths).items():
        _format(
            _paths,
            [
                UnsortedKeywordFinder(filetype),
                UnsortedCSVFinder(filetype),
            ],
            parse,
        )
