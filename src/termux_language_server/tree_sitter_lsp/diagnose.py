r"""Diagnose
============

Wrap
``Diagnostic <https://microsoft.github.io/language-server-protocol/specifications/specification-current#diagnostic>``_
to a linter.
"""
import sys
from typing import Callable, Literal

from lsprotocol.types import Diagnostic, DiagnosticSeverity
from tree_sitter import Tree

from . import Finder
from .utils import get_finders, get_paths


def get_diagnostics_by_finders(
    uri: str, tree: Tree, finders: list[Finder]
) -> list[Diagnostic]:
    r"""Get diagnostics by finders.

    :param uri:
    :type uri: str
    :param tree:
    :type tree: Tree
    :param finders:
    :type finders: list[Finder]
    :rtype: list[Diagnostic]
    """
    return [
        diagnostic
        for finder in finders
        for diagnostic in finder.get_diagnostics(uri, tree)
    ]


def get_diagnostics(
    uri: str,
    tree: Tree,
    classes: list[type[Finder]] | None = None,
    filetype: str | None = None,
) -> list[Diagnostic]:
    r"""Get diagnostics.

    :param uri:
    :type uri: str
    :param tree:
    :type tree: Tree
    :param classes:
    :type classes: list[type[Finder]] | None
    :param filetype:
    :type filetype: str | None
    :rtype: list[Diagnostic]
    """
    finders, finder_classes = get_finders(classes)
    if filetype is None:
        return get_diagnostics_by_finders(uri, tree, finders)
    return [
        diagnostic
        for diagnostic in get_diagnostics_by_finders(
            uri, tree, finders + [cls(filetype) for cls in finder_classes]
        )
    ]


def count_level(
    diagnostics: list[Diagnostic],
    level: DiagnosticSeverity = DiagnosticSeverity.Warning,
) -> int:
    r"""Count level.

    :param diagnostics:
    :type diagnostics: list[Diagnostic]
    :param level:
    :type level: DiagnosticSeverity
    :rtype: int
    """
    return len(
        [
            diagnostic
            for diagnostic in diagnostics
            if diagnostic.severity and diagnostic.severity <= level
        ]
    )


class _Colorama:
    """Colorama."""

    def __getattribute__(self, _: str) -> str:
        """Getattribute.

        :param _:
        :type _: str
        :rtype: str
        """
        return ""


def diagnostics2linter_messages(
    path: str,
    diagnostics: list[Diagnostic],
    color: Literal["auto", "always", "never"] = "auto",
    colors: list[str] | None = None,
) -> list[str]:
    r"""Diagnostics2linter messages.

    :param path:
    :type path: str
    :param diagnostics:
    :type diagnostics: list[Diagnostic]
    :param color:
    :type color: Literal["auto", "always", "never"]
    :param colors:
    :type colors: list[str] | None
    :rtype: list[str]
    """
    from colorama import Fore, init

    init()
    if not sys.stdout.isatty() and color == "auto" or color == "never":
        Fore = _Colorama()
    if colors is None:
        colors = [Fore.RESET, Fore.RED, Fore.YELLOW, Fore.BLUE, Fore.GREEN]
    return [
        f"{Fore.MAGENTA}{path}{Fore.RESET}:{Fore.CYAN}{diagnostic.range.start.line + 1}:{diagnostic.range.start.character + 1}{Fore.RESET}-{Fore.CYAN}{diagnostic.range.end.line + 1}:{diagnostic.range.end.character + 1}{Fore.RESET}:{colors[diagnostic.severity if diagnostic.severity else 0]}{str(diagnostic.severity).split('.')[-1].lower()}{Fore.RESET}: {diagnostic.message}"
        for diagnostic in diagnostics
    ]


def check_by_finders(
    paths: list[str],
    parse: Callable[[bytes], Tree],
    finders: list[Finder],
    color: Literal["auto", "always", "never"] = "auto",
) -> int:
    r"""Check by finders.

    :param paths:
    :type paths: list[str]
    :param parse:
    :type parse: Callable[[bytes], Tree]
    :param finders:
    :type finders: list[Finder]
    :param color:
    :type color: Literal["auto", "always", "never"]
    :rtype: int
    """
    count = 0
    lines = []
    for path in paths:
        with open(path, "rb") as f:
            src = f.read()
        tree = parse(src)
        diagnostics = get_diagnostics_by_finders(path, tree, finders)
        count += count_level(diagnostics)
        lines += diagnostics2linter_messages(path, diagnostics, color)
    if text := "\n".join(lines):
        print(text)
    return count


def check(
    paths: list[str],
    parse: Callable[[bytes], Tree],
    classes: list[type[Finder]] | None = None,
    get_filetype: Callable[[str], str] | None = None,
    color: Literal["auto", "always", "never"] = "auto",
) -> int:
    r"""Check.

    :param paths:
    :type paths: list[str]
    :param parse:
    :type parse: Callable[[bytes], Tree]
    :param classes:
    :type classes: list[type[Finder]] | None
    :param get_filetype:
    :type get_filetype: Callable[[str], str] | None
    :param color:
    :type color: Literal["auto", "always", "never"]
    :rtype: int
    """
    finders, finder_classes = get_finders(classes)
    if get_filetype is None:
        return check_by_finders(paths, parse, finders, color)
    return sum(
        check_by_finders(
            filepaths,
            parse,
            finders + [cls(filetype) for cls in finder_classes],
            color,
        )
        for filetype, filepaths in get_paths(paths, get_filetype).items()
    )
