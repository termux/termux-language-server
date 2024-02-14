r"""Namcap
==========
"""

from lsprotocol.types import Diagnostic, DiagnosticSeverity, Position, Range


def namcap(path: str, source: str) -> list[Diagnostic]:
    r"""Namcap.

    :param path:
    :type path: str
    :param source:
    :type source: str
    :rtype: list[Diagnostic]
    """
    try:
        from Namcap.rules import all_rules
    except ImportError:
        return []
    from Namcap.package import load_from_pkgbuild
    from Namcap.ruleclass import PkgbuildRule
    from Namcap.tags import format_message

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
