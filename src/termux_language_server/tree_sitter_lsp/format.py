r"""Format
==========
"""
from typing import Callable

from lsprotocol.types import Position, Range, TextEdit
from tree_sitter import Tree

from . import Finder


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


def format(
    paths: list[str], finders: list[Finder], parse: Callable[[bytes], Tree]
) -> None:
    r"""Format.

    :param paths:
    :type paths: list[str]
    :param finders:
    :type finders: list[Finder]
    :param parse:
    :type parse: Callable[[bytes], Tree]
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


def get_text_edits(
    finders: list[Finder], uri: str, tree: Tree
) -> list[TextEdit]:
    r"""Get text edits.

    :param finders:
    :type finders: list[Finder]
    :param uri:
    :type uri: str
    :param tree:
    :type tree: Tree
    :rtype: list[TextEdit]
    """
    return [
        text_edit
        for finder in finders
        for text_edit in finder.get_text_edits(uri, tree)
    ]
