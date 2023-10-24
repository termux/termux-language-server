r"""Schema
==========
"""
from dataclasses import dataclass
from typing import Any

from lsprotocol.types import Position, Range
from tree_sitter import Node, Tree

from . import UNI


@dataclass
class Trie:
    r"""Trie."""

    range: Range
    parent: "Trie | None" = None
    # can be serialized to a json
    value: dict[str, "Trie"] | list["Trie"] | str | int | float | None = None

    def get_root(self) -> "Trie":
        r"""Get root.

        :rtype: "Trie"
        """
        node = self
        while node.parent is not None:
            node = node.parent
        return node

    def to_path(self) -> str:
        r"""To path.

        :rtype: str
        """
        if self.parent is None:
            return "$"
        path = self.parent.to_path()
        if isinstance(self.parent.value, dict):
            for k, v in self.parent.value.items():
                if v is self:
                    return f"{path}.{k}"
            raise TypeError
        if isinstance(self.parent.value, list):
            for k, v in enumerate(self.parent.value):
                if v is self:
                    return f"{path}[{k}]"
            raise TypeError
        return path

    def from_path(self, path: str) -> "Trie":
        r"""From path.

        :param path:
        :type path: str
        :rtype: "Trie"
        """
        node = self
        if path.startswith("$"):
            path = path.lstrip("$")
            node = self.get_root()
        return node.from_relative_path(path)

    def from_relative_path(self, path: str) -> "Trie":
        r"""From relative path.

        :param path:
        :type path: str
        :rtype: "Trie"
        """
        if path == "":
            return self
        if path.startswith("."):
            if not isinstance(self.value, dict):
                raise TypeError
            path = path.lstrip(".")
            index, mid, path = path.partition(".")
            if mid == ".":
                path = mid + path
            index, mid, suffix = index.partition("[")
            if mid == "[":
                path = mid + suffix + path
            return self.value[index].from_relative_path(path)
        if path.startswith("["):
            if not isinstance(self.value, list):
                raise TypeError
            path = path.lstrip("[")
            index, _, path = path.partition("]")
            return self.value[int(index)].from_relative_path(path)
        raise TypeError

    def to_json(self) -> dict[str, Any] | list[Any] | str | int | float | None:
        r"""To json.

        :rtype: dict[str, Any] | list[Any] | str | int | float | None
        """
        if isinstance(self.value, dict):
            return {k: v.to_json() for k, v in self.value.items()}
        if isinstance(self.value, list):
            return [v.to_json() for v in self.value]
        return self.value

    @classmethod
    def from_tree(cls, tree: Tree) -> "Trie":
        r"""From tree.

        :param tree:
        :type tree: Tree
        :rtype: "Trie"
        """
        return cls.from_node(tree.root_node, None)

    @classmethod
    def from_node(cls, node: Node, parent: "Trie | None") -> "Trie":
        r"""From node.

        :param node:
        :type node: Node
        :param parent:
        :type parent: Trie | None
        :rtype: "Trie"
        """
        if parent is None:
            _range = Range(Position(0, 0), Position(1, 0))
        else:
            _range = UNI.node2range(node)
        trie = cls(_range, parent, {})
        trie.value = {
            UNI.node2text(child.children[0]): cls.from_node(child, trie)
            for child in node.children
        }
        return trie
