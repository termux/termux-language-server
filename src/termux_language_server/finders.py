r"""Finders
===========
"""
from copy import deepcopy

from jinja2 import Template
from lsprotocol.types import (
    Diagnostic,
    DiagnosticSeverity,
    DocumentLink,
    Position,
    Range,
    TextEdit,
)
from tree_sitter import Tree

from .tree_sitter_lsp import UNI, Finder
from .tree_sitter_lsp.finders import RequiresFinder, UnFixedOrderFinder


class InvalidNodeFinder(Finder):
    r"""Invalidnodefinder."""

    def __init__(
        self,
        names: set[str],
        message: str = "{{uni.get_text()}}: shouldn't be {{type}}",
        severity: DiagnosticSeverity = DiagnosticSeverity.Error,
    ) -> None:
        r"""Init.

        :param names:
        :type names: set[str]
        :param message:
        :type message: str
        :param severity:
        :type severity: DiagnosticSeverity
        :rtype: None
        """
        super().__init__(message, severity)
        self.names = names

    @staticmethod
    def is_correct_uni_without_expansion(uni: UNI) -> bool:
        r"""Is correct uni without expansion.

        :param uni:
        :type uni: UNI
        :rtype: bool
        """
        parent = uni.node.parent
        if parent is None:
            return False
        text = uni.get_text()
        return (
            text.isupper()
            and uni.node.type == "variable_name"
            and parent.type == "variable_assignment"
            or text.islower()
            and parent.type == "function_definition"
        )

    @staticmethod
    def is_array(uni: UNI) -> bool:
        r"""Is array.

        :param uni:
        :type uni: UNI
        :rtype: bool
        """
        text = uni.get_text()
        parent = uni.node.parent
        if parent is None:
            return False
        if (
            text.isupper()
            and uni.node.type == "variable_name"
            and parent.type == "variable_assignment"
            and parent.children[-1].type == "array"
        ):
            return True
        return False

    @staticmethod
    def is_correct_uni(uni: UNI) -> bool:
        r"""Is correct uni.

        :param uni:
        :type uni: UNI
        :rtype: bool
        """
        text = uni.get_text()
        parent = uni.node.parent
        if parent is None:
            return False
        return (
            InvalidNodeFinder.is_correct_uni_without_expansion(uni)
            or text.isupper()
            and parent.type == "expansion"
            or text.islower()
            and parent.type == "command"
        )

    def __call__(self, uni: UNI) -> bool:
        r"""Call.

        :param uni:
        :type uni: UNI
        :rtype: bool
        """
        text = uni.get_text()
        return text in self.names and (
            not self.is_correct_uni(uni) or self.is_array(uni)
        )

    def uni2diagnostic(self, uni: UNI) -> Diagnostic:
        r"""Uni2diagnostic.

        :param uni:
        :type uni: UNI
        :rtype: Diagnostic
        """
        parent = uni.node.parent
        if parent is None:
            raise TypeError
        _type = parent.type
        if self.is_array(uni):
            _type = "array"
        return uni.get_diagnostic(self.message, self.severity, type=_type)


class RequireNodesFinder(RequiresFinder):
    r"""Requirenodesfinder."""

    def filter(self, uni: UNI, require: str) -> bool:
        r"""Filter.

        :param uni:
        :type uni: UNI
        :param require:
        :type require: str
        :rtype: bool
        """
        text = uni.get_text()
        return (
            text == require
            and InvalidNodeFinder.is_correct_uni_without_expansion(uni)
        )


class UnsortedNodesFinder(UnFixedOrderFinder):
    r"""Unsortednodesfinder."""

    def filter(self, uni: UNI) -> bool:
        r"""Filter.

        :param uni:
        :type uni: UNI
        :rtype: bool
        """
        text = uni.get_text()
        return (
            text in self.order
            and InvalidNodeFinder.is_correct_uni_without_expansion(uni)
        )

    def get_text_edits(self, uri: str, tree: Tree) -> list[TextEdit]:
        r"""Get text edits. Only return two to avoid `Overlapping edit`

        :param self:
        :param uri:
        :type uri: str
        :param tree:
        :type tree: Tree
        :rtype: list[TextEdit]
        """
        self.find_all(uri, tree)
        for uni, _uni in self.uni_pairs:
            parent = uni.node.parent
            _parent = _uni.node.parent
            if parent is None or _parent is None:
                return []
            # swap 2 unis
            return [
                TextEdit(UNI.node2range(parent), UNI.node2text(_parent)),
                TextEdit(UNI.node2range(_parent), UNI.node2text(parent)),
            ]
        return []


class PackageFinder(Finder):
    r"""Packagefinder."""

    def __init__(self, csvs: set[str]) -> None:
        r"""Init.

        :param csvs:
        :type csvs: set[str]
        :rtype: None
        """
        super().__init__()
        self.csvs = csvs - {"TERMUX_PKG_BLACKLISTED_ARCHES"}

    def __call__(self, uni: UNI) -> bool:
        r"""Call.

        :param uni:
        :type uni: UNI
        :rtype: bool
        """
        parent = uni.node.parent
        if parent is None:
            return False
        return (
            parent.type == "variable_assignment"
            and uni.node == parent.children[-1]
            and UNI.node2text(parent.children[0]) in self.csvs
        )

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
        links = []
        for uni in self.find_all(uri, tree):
            start = list(uni.node.start_point)
            text = uni.get_text()
            if text.startswith('"'):
                text = text.strip('"')
                start[1] += 1
            end = deepcopy(start)
            for name in text.split(","):
                if name.startswith(" "):
                    name = name.lstrip(" ")
                    start[1] += 1
                    end[1] += 1
                end[1] += len(name)
                links += [
                    DocumentLink(
                        Range(Position(*start), Position(*end)),
                        Template(template).render(name=name),
                    )
                ]
                start[1] += len(name) + 1
        return links
