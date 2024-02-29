r"""Schema
==========
"""

from dataclasses import dataclass
from typing import Literal

from lsp_tree_sitter import UNI
from lsp_tree_sitter.schema import Trie
from lsprotocol.types import Position, Range
from tree_sitter import Node


@dataclass
class BashTrie(Trie):
    r"""Bashtrie."""

    value: dict[str, "Trie"] | list["Trie"] | str | Literal[0] = 0

    @classmethod
    def from_string_node(cls, node: Node, parent: "Trie | None") -> "Trie":
        r"""From string node.

        `<https://github.com/tree-sitter/tree-sitter-bash/issues/101>`_

        :param cls:
        :param node:
        :type node: Node
        :param parent:
        :type parent: Trie | None
        :rtype: "Trie"
        """
        if node.type == "string" and node.children == 3:
            node = node.children[1]
        text = UNI.node2text(node)
        _range = UNI.node2range(node)
        if node.type in {"string", "raw_string"} and node.children != 3:
            text = text.strip("'\"")
            _range.start.character += 1
            _range.end.character -= 1
        return cls(_range, parent, text)

    @classmethod
    def from_node(cls, node: Node, parent: "Trie | None") -> "Trie":
        r"""From node.

        :param node:
        :type node: Node
        :param parent:
        :type parent: Trie | None
        :rtype: "Trie"
        """
        string_types = {
            "word",
            "string",
            "raw_string",
            "concatenation",
            "number",
            "simple_expansion",
        }
        if node.type in string_types:
            return cls.from_string_node(node, parent)
        if node.type == "function_definition":
            return cls(UNI.node2range(node), parent, 0)
        if node.type == "variable_assignment":
            if len(node.children) < 3:
                return cls(UNI.node2range(node), parent, "")
            node = node.children[2]
            if node.type == "array":
                trie = cls(UNI.node2range(node), parent, [])
                value: list[Trie] = trie.value  # type: ignore
                trie.value = [
                    cls.from_node(child, trie)
                    for child in node.children
                    if child.type in string_types
                ]
                return trie
            if node.type in string_types:
                return cls.from_string_node(node, parent)
        if node.type == "program":
            trie = cls(Range(Position(0, 0), Position(1, 0)), parent, {})
            value: dict[str, Trie] = trie.value  # type: ignore
            for child in node.children:
                if child.type in {
                    "variable_assignment",
                    "function_definition",
                }:
                    value[UNI.node2text(child.children[0])] = cls.from_node(
                        child, trie
                    )
            return trie
        raise NotImplementedError(node.type)
