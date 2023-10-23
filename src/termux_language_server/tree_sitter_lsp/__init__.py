r"""Tree-sitter LSP
===================
"""
import os
from copy import deepcopy
from dataclasses import dataclass
from typing import Any

from jinja2 import Template
from lsprotocol.types import (
    Diagnostic,
    DiagnosticSeverity,
    DocumentLink,
    Location,
    Position,
    Range,
    TextEdit,
)
from pygls.uris import to_fs_path
from tree_sitter import Node, Tree, TreeCursor

# maximum of recursive search
LEVEL = 5


@dataclass
class UNI:
    r"""Unified node identifier."""

    uri: str
    node: Node

    def __str__(self) -> str:
        r"""Str.

        :rtype: str
        """
        return f"{self.get_text()}@{self.uri}:{self.node.start_point[0] + 1}:{self.node.start_point[1] + 1}-{self.node.end_point[0] + 1}:{self.node.end_point[1]}"

    def get_text(self) -> str:
        r"""Get text.

        :rtype: str
        """
        return self.node2text(self.node)

    @staticmethod
    def node2text(node: Node) -> str:
        r"""Node2text.

        :param node:
        :type node: Node
        :rtype: str
        """
        return node.text.decode()

    def get_location(self) -> Location:
        r"""Get location.

        :rtype: Location
        """
        return Location(self.uri, self.get_range())

    def get_range(self) -> Range:
        r"""Get range.

        :rtype: Range
        """
        return self.node2range(self.node)

    @staticmethod
    def node2range(node: Node) -> Range:
        r"""Node2range.

        :param node:
        :type node: Node
        :rtype: Range
        """
        return Range(Position(*node.start_point), Position(*node.end_point))

    def get_path(self) -> str:
        r"""Get path.

        :rtype: str
        """
        return self.uri2path(self.uri)

    @staticmethod
    def uri2path(uri: str) -> str:
        r"""Uri2path.

        :param uri:
        :type uri: str
        :rtype: str
        """
        if path := to_fs_path(uri):
            return path
        raise TypeError

    def get_diagnostic(
        self,
        message: str,
        severity: DiagnosticSeverity,
        **kwargs: Any,
    ) -> Diagnostic:
        r"""Get diagnostic.

        :param message:
        :type message: str
        :param severity:
        :type severity: DiagnosticSeverity
        :param kwargs:
        :type kwargs: Any
        :rtype: Diagnostic
        """
        _range = self.get_range()
        _range.end.character -= 1
        return Diagnostic(
            _range,
            Template(message).render(uni=self, **kwargs),
            severity,
        )

    def get_text_edit(self, new_text: str) -> TextEdit:
        r"""Get text edit.

        :param new_text:
        :type new_text: str
        :rtype: TextEdit
        """
        return TextEdit(self.get_range(), new_text)

    def get_document_link(self, target: str, **kwargs) -> DocumentLink:
        r"""Get document link.

        :param target:
        :type target: str
        :param kwargs:
        :rtype: DocumentLink
        """
        return DocumentLink(
            self.get_range(),
            Template(target).render(uni=self, **kwargs),
        )

    @staticmethod
    def join(path, text) -> str:
        r"""Join.

        :param path:
        :param text:
        :rtype: str
        """
        return os.path.join(os.path.dirname(path), text)


@dataclass
class Finder:
    r"""Finder."""

    message: str = ""
    severity: DiagnosticSeverity = DiagnosticSeverity.Error

    def __post_init__(self) -> None:
        r"""Post init.

        :rtype: None
        """
        self.reset()

    def __call__(self, uni: UNI) -> bool:
        r"""Call.

        :param uni:
        :type uni: UNI
        :rtype: bool
        """
        return True

    def __and__(self, second: "Finder") -> "Finder":
        r"""And.

        :param second:
        :type second: Finder
        :rtype: "Finder"
        """
        finder = deepcopy(self)
        finder.__call__ = lambda uni: self(uni) and second(uni)
        return finder

    def __or__(self, second: "Finder") -> "Finder":
        r"""Or.

        :param second:
        :type second: Finder
        :rtype: "Finder"
        """
        finder = deepcopy(self)
        finder.__call__ = lambda uni: self(uni) or second(uni)
        return finder

    def __minus__(self, second: "Finder") -> "Finder":
        r"""Minus.

        :param second:
        :type second: Finder
        :rtype: "Finder"
        """
        finder = deepcopy(self)
        finder.__call__ = lambda uni: self(uni) and not second(uni)
        return finder

    def is_include_node(self, node: Node) -> bool:
        r"""Is include node.

        :param node:
        :type node: Node
        :rtype: bool
        """
        return False

    def parse(self, code: bytes) -> Tree:
        r"""Parse.

        :param code:
        :type code: bytes
        :rtype: Tree
        """
        raise NotImplementedError

    def uri2tree(self, uri: str) -> Tree | None:
        r"""Convert URI to tree.

        :param uri:
        :type uri: str
        :rtype: Tree | None
        """
        path = UNI.uri2path(uri)
        if not os.path.exists(path):
            return None
        with open(path, "rb") as f:
            code = f.read()
        return self.parse(code)

    def uni2uri(self, uni: UNI) -> str:
        r"""Convert UNI to URI.

        :param uni:
        :type uni: UNI
        :rtype: str
        """
        return uni.join(uni.uri, uni.get_text())

    def uni2path(self, uni: UNI) -> str:
        r"""Convert UNI to path.

        :param self:
        :param uni:
        :type uni: UNI
        :rtype: str
        """
        uri = self.uni2uri(uni)
        return UNI.uri2path(uri)

    def move_cursor(
        self, uri: str, cursor: TreeCursor, is_all: bool = False
    ) -> str | None:
        r"""Move cursor.

        :param self:
        :param uri:
        :type uri: str
        :param cursor:
        :type cursor: TreeCursor
        :param is_all:
        :type is_all: bool
        :rtype: str | None
        """
        while self(UNI(uri, cursor.node)) is False:
            if self.is_include_node(cursor.node) and self.level < LEVEL:
                self.level += 1
                old_uri = uri
                uri = self.uni2uri(UNI(uri, cursor.node))
                tree = self.uri2tree(uri)
                if tree is not None:
                    if is_all:
                        self.find_all(uri, tree, False)
                    else:
                        result = self.find(uri, tree)
                        if result is not None:
                            return
                uri = old_uri
                self.level -= 1
            if cursor.node.child_count > 0:
                cursor.goto_first_child()
                continue
            while cursor.node.next_sibling is None:
                cursor.goto_parent()
                # when cannot find new nodes, return
                if cursor.node.parent is None:
                    return None
            cursor.goto_next_sibling()
        return uri

    def reset(self) -> None:
        r"""Reset.

        :rtype: None
        """
        self.level = 0
        self.unis = []

    def prepare(
        self, uri: str, tree: Tree | None = None, reset: bool = True
    ) -> TreeCursor:
        r"""Prepare.

        :param uri:
        :type uri: str
        :param tree:
        :type tree: Tree | None
        :param reset:
        :type reset: bool
        :rtype: TreeCursor
        """
        if reset:
            self.reset()
        if tree is None:
            tree = self.uri2tree(uri)
        if tree is None:
            raise TypeError
        return tree.walk()

    def find(
        self, uri: str, tree: Tree | None = None, reset: bool = True
    ) -> UNI | None:
        r"""Find.

        :param uri:
        :type uri: str
        :param tree:
        :type tree: Tree | None
        :param reset:
        :type reset: bool
        :rtype: UNI | None
        """
        cursor = self.prepare(uri, tree, reset)
        _uri = self.move_cursor(uri, cursor, False)
        if _uri is not None:
            return UNI(_uri, cursor.node)
        else:
            return None

    def find_all(
        self, uri: str, tree: Tree | None = None, reset: bool = True
    ) -> list[UNI]:
        r"""Find all.

        :param uri:
        :type uri: str
        :param tree:
        :type tree: Tree | None
        :param reset:
        :type reset: bool
        :rtype: list[UNI]
        """
        cursor = self.prepare(uri, tree, reset)
        while True:
            _uri = self.move_cursor(uri, cursor, True)
            if _uri is not None:
                self.unis += [UNI(_uri, cursor.node)]
            while cursor.node.next_sibling is None:
                cursor.goto_parent()
                # when cannot find new nodes, return
                if cursor.node.parent is None:
                    return self.unis
            cursor.goto_next_sibling()

    def uni2diagnostic(self, uni: UNI) -> Diagnostic:
        r"""Uni2diagnostic.

        :param uni:
        :type uni: UNI
        :rtype: Diagnostic
        """
        return uni.get_diagnostic(self.message, self.severity)

    def unis2diagnostics(self, unis: list[UNI]) -> list[Diagnostic]:
        r"""Unis2diagnostics.

        :param unis:
        :type unis: list[UNI]
        :rtype: list[Diagnostic]
        """
        return [self.uni2diagnostic(uni) for uni in unis]

    def get_diagnostics(self, uri: str, tree: Tree) -> list[Diagnostic]:
        r"""Get diagnostics.

        :param self:
        :param uri:
        :type uri: str
        :param tree:
        :type tree: Tree
        :rtype: list[Diagnostic]
        """
        return self.unis2diagnostics(self.find_all(uri, tree))

    def get_text_edits(self, uri: str, tree: Tree) -> list[TextEdit]:
        r"""Get text edits.

        :param self:
        :param uri:
        :type uri: str
        :param tree:
        :type tree: Tree
        :rtype: list[TextEdit]
        """
        self.find_all(uri, tree)
        return []

    def get_document_links(
        self, uri: str, tree: Tree, template: str
    ) -> list[DocumentLink]:
        r"""Get document links.

        :param uri:
        :type uri: str
        :param tree:
        :type tree: Tree
        :param template:
        :type template: str
        :rtype: list[DocumentLink]
        """
        self.find_all(uri, tree)
        return [
            uni.get_document_link(template) for uni in self.find_all(uri, tree)
        ]
