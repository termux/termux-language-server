r"""Utils
=========
"""
from typing import Callable, Literal

from tree_sitter import Tree

from .documents import get_filetype
from .finders import BashFinder, UnsortedCSVFinder, UnsortedKeywordFinder
from .tree_sitter_lsp.diagnose import check
from .tree_sitter_lsp.finders import ErrorFinder, MissingFinder
from .tree_sitter_lsp.format import format
from .tree_sitter_lsp.utils import get_paths

DIAGNOSTICS_FINDERS = [
    ErrorFinder(),
    MissingFinder(),
]


def check_by_filetype(
    paths: list[str],
    parse: Callable[[bytes], Tree],
    color: Literal["auto", "always", "never"] = "auto",
) -> int:
    r"""Check by filetype.

    :param paths:
    :type paths: list[str]
    :param parse:
    :type parse: Callable[[bytes], Tree]
    :param color:
    :type color: Literal["auto", "always", "never"]
    :rtype: int
    """
    return sum(
        check(
            _paths,
            DIAGNOSTICS_FINDERS
            + [
                BashFinder(filetype),
                UnsortedKeywordFinder(filetype),
                UnsortedCSVFinder(filetype),
            ],
            parse,
            color,
        )
        for filetype, _paths in get_paths(paths, get_filetype).items()
    )


def format_by_filetype(
    paths: list[str],
    parse: Callable[[bytes], Tree],
) -> None:
    r"""Format by filetype.

    :param paths:
    :type paths: list[str]
    :param parse:
    :type parse: Callable[[bytes], Tree]
    :rtype: None
    """
    for filetype, _paths in get_paths(paths, get_filetype).items():
        format(
            _paths,
            [
                UnsortedKeywordFinder(filetype),
                UnsortedCSVFinder(filetype),
            ],
            parse,
        )
