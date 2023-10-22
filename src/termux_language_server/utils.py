r"""Utils
=========
"""
from .tree_sitter_lsp.finders import ErrorFinder, MissingFinder

DIAGNOSTICS_FINDERS = [
    ErrorFinder(),
    MissingFinder(),
]
