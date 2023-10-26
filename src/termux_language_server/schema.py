r"""Schema
==========
"""
from dataclasses import dataclass
from typing import Literal

from lsprotocol.types import Position, Range
from tree_sitter import Node
from tree_sitter_lsp import UNI
from tree_sitter_lsp.schema import Trie


@dataclass
class BashTrie(Trie):
    r"""Bashtrie."""

    value: dict[str, "Trie"] | list["Trie"] | str | Literal[0] = 0

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
            "concatenation",
            "number",
            "simple_expansion",
        }
        if node.type in string_types:
            return cls(UNI.node2range(node), parent, UNI.node2text(node))
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
                return cls(UNI.node2range(node), parent, UNI.node2text(node))
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
