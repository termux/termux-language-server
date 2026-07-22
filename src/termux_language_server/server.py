r"""Server
==========
"""

import json
import os
from contextlib import suppress

from lsp_tree_sitter.completer import PackageCompleter, ValueCompleter
from lsp_tree_sitter.linter import PackageLinter, SchemaLinter
from lsp_tree_sitter.node import PackageSearcher
from lsp_tree_sitter.server import TreeSitterLanguageServer
from tree_sitter import Language, Parser
from tree_sitter_bash import language as get_language_ptr

from . import queries


class TermuxLanguageServer(TreeSitterLanguageServer):
    def __init__(self, *args, **kwargs) -> None:
        parser = Parser()
        language = Language(get_language_ptr())
        parser.language = language

        assets_path = os.path.join(os.path.dirname(__file__), "assets")
        self.schemas = {}
        json_path = os.path.join(assets_path, "json")
        for file in os.listdir(json_path):
            schema_name = file.rpartition(".")[0]
            with open(os.path.join(json_path, file)) as f:
                self.schemas[schema_name] = json.load(f)

        schema_linter = SchemaLinter.from_queries(
            language, queries, self.schema_getter
        )
        package_linter = PackageLinter.from_queries(
            language, queries, self.searcher_getter
        )
        code_file = os.path.join(assets_path, "jq", "value.jq")
        value_completer = ValueCompleter.from_files(
            code_file, self.schema_getter, "^"
        )
        self.searchers = self.get_searchers()
        package_completer = PackageCompleter(self.searcher_getter)

        super().__init__(
            parser,
            (schema_linter, package_linter),
            (value_completer, package_completer),
            *args,
            **kwargs,
        )
        with suppress(ImportError):
            from .linter import NamcapLinter

            self.linters += (NamcapLinter(),)

    def schema_getter(self, path: str):
        name = PackageSearcher.get_filetype(path, self.schemas)
        return self.schemas.get(name)

    def searcher_getter(self, path: str) -> PackageSearcher | None:
        name = PackageSearcher.get_filetype(path, self.searchers)
        return self.searchers.get(name)

    @staticmethod
    def get_searchers() -> dict[str, PackageSearcher]:
        searchers = {}
        with suppress(ImportError):
            from .searcher.pacman import PacmanSearcher

            searchers["PKGBUILD"] = PacmanSearcher()
        with suppress(ImportError):
            from .searcher.portage import PortageSearcher

            searchers["_ebuild"] = PortageSearcher()
        return searchers
