r"""Format
==========

Wrap
``Document Formatting <https://microsoft.github.io/language-server-protocol/specifications/specification-current#textDocument_formatting>``_
to a formatter.
"""
from typing import Callable

from lsprotocol.types import Position, Range, TextEdit
from tree_sitter import Tree

from . import Finder
from .utils import get_finders, get_paths


def position_2d_to_1d(source: str, position: Position) -> int:
    r"""Position 2d to 1d.

    :param source:
    :type source: str
    :param position:
    :type position: Position
    :rtype: int
    """
    return (
        sum(len(line) + 1 for line in source.splitlines()[: position.line])
        + position.character
    )


def range_2d_to_1d(source: str, region: Range) -> range:
    r"""Range 2d to 1d.

    :param source:
    :type source: str
    :param region:
    :type region: Range
    :rtype: range
    """
    return range(
        position_2d_to_1d(source, region.start),
        position_2d_to_1d(source, region.end),
    )


def apply_text_edits(text_edits: list[TextEdit], source: str) -> str:
    r"""Apply text edits.

    :param text_edits:
    :type text_edits: list[TextEdit]
    :param source:
    :type source: str
    :rtype: str
    """
    for text_edit in text_edits:
        region = range_2d_to_1d(source, text_edit.range)
        source = (
            source[: region.start] + text_edit.new_text + source[region.stop :]
        )
    return source


def format_by_finders(
    paths: list[str], parse: Callable[[bytes], Tree], finders: list[Finder]
) -> None:
    r"""Format by finders.

    :param paths:
    :type paths: list[str]
    :param parse:
    :type parse: Callable[[bytes], Tree]
    :param finders:
    :type finders: list[Finder]
    :rtype: None
    """
    for path in paths:
        with open(path, "rb") as f:
            src = f.read()
        tree = parse(src)
        text_edits = [
            text_edit
            for finder in finders
            for text_edit in finder.get_text_edits(path, tree)
        ]
        src = apply_text_edits(text_edits, src.decode())
        with open(path, "w") as f:
            f.write(src)


def get_text_edits_by_finders(
    uri: str, tree: Tree, finders: list[Finder]
) -> list[TextEdit]:
    r"""Get text edits by finders.

    :param uri:
    :type uri: str
    :param tree:
    :type tree: Tree
    :param finders:
    :type finders: list[Finder]
    :rtype: list[TextEdit]
    """
    return [
        text_edit
        for finder in finders
        for text_edit in finder.get_text_edits(uri, tree)
    ]


def get_text_edits(
    uri: str,
    tree: Tree,
    classes: list[type[Finder]] | None = None,
    filetype: str | None = None,
) -> list[TextEdit]:
    r"""Get text edits.

    :param uri:
    :type uri: str
    :param tree:
    :type tree: Tree
    :param classes:
    :type classes: list[type[Finder]] | None
    :param filetype:
    :type filetype: str | None
    :rtype: list[TextEdit]
    """
    finders, finder_classes = get_finders(classes)
    if filetype is None:
        return get_text_edits_by_finders(uri, tree, finders)
    return [
        text_edit
        for text_edit in get_text_edits_by_finders(
            uri, tree, finders + [cls(filetype) for cls in finder_classes]
        )
    ]


def format(
    paths: list[str],
    parse: Callable[[bytes], Tree],
    classes: list[type[Finder]] | None = None,
    get_filetype: Callable[[str], str] | None = None,
) -> None:
    r"""Format.

    :param paths:
    :type paths: list[str]
    :param parse:
    :type parse: Callable[[bytes], Tree]
    :param classes:
    :type classes: list[type[Finder]] | None
    :param get_filetype:
    :type get_filetype: Callable[[str], str] | None
    :rtype: None
    """
    finders, finder_classes = get_finders(classes)
    if get_filetype is None:
        return format_by_finders(paths, parse, finders)
    for filetype, filepaths in get_paths(paths, get_filetype).items():
        format_by_finders(
            filepaths,
            parse,
            finders + [cls(filetype) for cls in finder_classes],
        )
