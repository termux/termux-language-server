r"""Diagnose
============
"""
import sys
from typing import Callable, Literal

from lsprotocol.types import Diagnostic, DiagnosticSeverity
from tree_sitter import Tree

from . import Finder


def get_diagnostics(
    finders: list[Finder], uri: str, tree: Tree
) -> list[Diagnostic]:
    r"""Get diagnostics.

    :param finders:
    :type finders: list[Finder]
    :param uri:
    :type uri: str
    :param tree:
    :type tree: Tree
    :rtype: list[Diagnostic]
    """
    return [
        diagnostic
        for finder in finders
        for diagnostic in finder.get_diagnostics(uri, tree)
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


def check(
    paths: list[str],
    finders: list[Finder],
    parse: Callable[[bytes], Tree],
    color: Literal["auto", "always", "never"] = "auto",
) -> int:
    r"""Check.

    :param paths:
    :type paths: list[str]
    :param finders:
    :type finders: list[Finder]
    :param parse:
    :type parse: Callable[[bytes], Tree]
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
        diagnostics = get_diagnostics(finders, path, tree)
        count += count_level(diagnostics)
        lines += diagnostics2linter_messages(path, diagnostics, color)
    print("\n".join(lines))
    return count
