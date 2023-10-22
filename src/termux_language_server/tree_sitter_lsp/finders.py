r"""Finders
===========
"""
import os

from lsprotocol.types import (
    Diagnostic,
    DiagnosticSeverity,
    Location,
    Position,
    Range,
    TextEdit,
)
from tree_sitter import Node

from . import UNI, Finder


class MissingFinder(Finder):
    r"""Missingfinder."""

    def __init__(
        self,
        message: str = "{{uni.get_text()}}: missing",
        severity: DiagnosticSeverity = DiagnosticSeverity.Error,
    ) -> None:
        r"""Init.

        :param message:
        :type message: str
        :param severity:
        :type severity: DiagnosticSeverity
        :rtype: None
        """
        super().__init__(message, severity)

    def __call__(self, uni: UNI) -> bool:
        r"""Call.

        :param uni:
        :type uni: UNI
        :rtype: bool
        """
        node = uni.node
        return node.is_missing and not (
            any(child.is_missing for child in node.children)
        )


class ErrorFinder(Finder):
    r"""Errorfinder."""

    def __init__(
        self,
        message: str = "{{uni.get_text()}}: error",
        severity: DiagnosticSeverity = DiagnosticSeverity.Error,
    ) -> None:
        r"""Init.

        :param message:
        :type message: str
        :param severity:
        :type severity: DiagnosticSeverity
        :rtype: None
        """
        super().__init__(message, severity)

    def __call__(self, uni: UNI) -> bool:
        r"""Call.

        :param uni:
        :type uni: UNI
        :rtype: bool
        """
        node = uni.node
        return node.has_error and not (
            any(child.has_error for child in node.children)
        )


class NotFileFinder(Finder):
    r"""NotFilefinder."""

    def __init__(
        self,
        message: str = "{{uni.get_text()}}: no such file or directory",
        severity: DiagnosticSeverity = DiagnosticSeverity.Error,
    ) -> None:
        r"""Init.

        :param message:
        :type message: str
        :param severity:
        :type severity: DiagnosticSeverity
        :rtype: None
        """
        super().__init__(message, severity)

    def __call__(self, uni: UNI) -> bool:
        r"""Call.

        :param uni:
        :type uni: UNI
        :rtype: bool
        """
        path = self.uni2path(uni)
        return not (os.path.isfile(path) or os.path.isdir(path))


class RepeatedFinder(Finder):
    r"""Repeatedfinder."""

    def __init__(
        self,
        message: str = "{{uni.get_text()}}: is repeated on {{_uni}}",
        severity: DiagnosticSeverity = DiagnosticSeverity.Warning,
    ) -> None:
        r"""Init.

        :param message:
        :type message: str
        :param severity:
        :type severity: DiagnosticSeverity
        :rtype: None
        """
        super().__init__(message, severity)

    def reset(self) -> None:
        r"""Reset.

        :rtype: None
        """
        self.unis = []
        self._unis = []
        self.uni_pairs = []

    def filter(self, uni: UNI) -> bool:
        r"""Filter.

        :param uni:
        :type uni: UNI
        :rtype: bool
        """
        return True

    def compare(self, uni: UNI, _uni: UNI) -> bool:
        r"""Compare.

        :param uni:
        :type uni: UNI
        :param _uni:
        :type _uni: UNI
        :rtype: bool
        """
        return uni.node.text == _uni.node.text

    def __call__(self, uni: UNI) -> bool:
        r"""Call.

        :param uni:
        :type uni: UNI
        :rtype: bool
        """
        if self.filter(uni) is False:
            return False
        for _uni in self._unis:
            if self.compare(uni, _uni):
                self.uni_pairs += [[uni, _uni]]
                return True
        self._unis += [uni]
        return False

    def get_definitions(self, uni: UNI) -> list[Location]:
        r"""Get definitions.

        :param uni:
        :type uni: UNI
        :rtype: list[Location]
        """
        for uni_, _uni in self.uni_pairs:
            # cache hit
            if uni == uni_:
                return [_uni.get_location()]
        return []

    def get_references(self, uni: UNI) -> list[Location]:
        r"""Get references.

        :param uni:
        :type uni: UNI
        :rtype: list[Location]
        """
        locations = []
        for uni_, _uni in self.uni_pairs:
            # cache hit
            if uni == _uni:
                locations += [uni_.get_location()]
        return locations

    def get_text_edits(self) -> list[TextEdit]:
        r"""Get text edits.

        :rtype: list[TextEdit]
        """
        edits = []
        for uni, _uni in self.uni_pairs:
            # swap 2 unis
            edits += [
                uni.get_text_edit(_uni.get_text()),
                _uni.get_text_edit(uni.get_text()),
            ]
        return edits

    def uni2diagnostic(self, uni: UNI) -> Diagnostic:
        r"""Uni2diagnostic.

        :param uni:
        :type uni: UNI
        :rtype: Diagnostic
        """
        for uni_, _uni in self.uni_pairs:
            if uni == uni_:
                return uni.get_diagnostic(
                    self.message, self.severity, _uni=_uni
                )
        return uni.get_diagnostic(self.message, self.severity)


class UnsortedFinder(RepeatedFinder):
    r"""Unsortedfinder."""

    def __init__(
        self,
        message: str = "{{uni.get_text()}}: is unsorted due to {{_uni}}",
        severity: DiagnosticSeverity = DiagnosticSeverity.Warning,
    ) -> None:
        r"""Init.

        :param message:
        :type message: str
        :param severity:
        :type severity: DiagnosticSeverity
        :rtype: None
        """
        super().__init__(message, severity)

    def compare(self, uni: UNI, _uni: UNI) -> bool:
        r"""Compare.

        :param uni:
        :type uni: UNI
        :param _uni:
        :type _uni: UNI
        :rtype: bool
        """
        return uni.node.text < _uni.node.text


class TypeFinder(Finder):
    r"""Typefinder."""

    def __init__(
        self,
        _type: str,
        message: str = "",
        severity: DiagnosticSeverity = DiagnosticSeverity.Information,
    ) -> None:
        r"""Init.

        :param self:
        :param _type:
        :type _type: str
        :param message:
        :type message: str
        :param severity:
        :type severity: DiagnosticSeverity
        :rtype: None
        """
        super().__init__(message, severity)
        self.type = _type

    def __call__(self, uni: UNI) -> bool:
        r"""Call.

        :param uni:
        :type uni: UNI
        :rtype: bool
        """
        node = uni.node
        return node.type == self.type


class PositionFinder(Finder):
    r"""Positionfinder."""

    def __init__(self, position: Position) -> None:
        r"""Init.

        :param position:
        :type position: Position
        :rtype: None
        """
        super().__init__()
        self.position = position

    @staticmethod
    def belong(position: Position, node: Node) -> bool:
        r"""Belong.

        :param position:
        :type position: Position
        :param node:
        :type node: Node
        :rtype: bool
        """
        return (
            Position(*node.start_point) <= position < Position(*node.end_point)
        )

    def __call__(self, uni: UNI) -> bool:
        r"""Call.

        :param uni:
        :type uni: UNI
        :rtype: bool
        """
        node = uni.node
        return node.child_count == 0 and self.belong(self.position, node)


class RangeFinder(Finder):
    r"""Rangefinder."""

    def __init__(self, _range: Range) -> None:
        r"""Init.

        :param _range:
        :type _range: Range
        :rtype: None
        """
        super().__init__()
        self.range = _range

    @staticmethod
    def equal(_range: Range, node: Node) -> bool:
        r"""Equal.

        :param _range:
        :type _range: Range
        :param node:
        :type node: Node
        :rtype: bool
        """
        return _range.start == Position(
            *node.start_point
        ) and _range.end == Position(*node.end_point)

    def __call__(self, uni: UNI) -> bool:
        r"""Call.

        :param uni:
        :type uni: UNI
        :rtype: bool
        """
        node = uni.node
        return self.equal(self.range, node)
