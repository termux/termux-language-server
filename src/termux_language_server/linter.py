r"""Namcap
==========
"""

from dataclasses import dataclass
from typing import TYPE_CHECKING

from lsp_tree_sitter.linter import LinterBase
from lsp_tree_sitter.node import NodeText
from lsprotocol.types import (
    Diagnostic,
    DiagnosticSeverity,
    DocumentLink,
    Position,
    Range,
)
from Namcap.package import load_from_pkgbuild
from Namcap.ruleclass import PkgbuildRule
from Namcap.rules import all_rules
from Namcap.tags import format_message

if TYPE_CHECKING:
    from tree_sitter import Tree


@dataclass
class NamcapLinter(LinterBase):
    def link(self, tree: "Tree", path: str) -> list[DocumentLink]:
        return []

    def diagnose(self, tree: "Tree", path: str) -> list[Diagnostic]:
        source = NodeText(tree.root_node)
        pkginfo = load_from_pkgbuild(path)
        items = {}
        for value in all_rules.values():
            rule = value()
            if isinstance(rule, PkgbuildRule):
                rule.analyze(pkginfo, "PKGBUILD")  # type: ignore
            for msg in rule.errors:
                items[format_message(msg)] = DiagnosticSeverity.Error
            for msg in rule.warnings:
                items[format_message(msg)] = DiagnosticSeverity.Warning
        end = len(source.splitlines()[0])
        return [
            Diagnostic(Range(Position(0, 0), Position(0, end)), msg, severity)
            for msg, severity in items.items()
        ]
