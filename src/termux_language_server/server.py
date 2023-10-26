r"""Server
==========
"""
import re
from typing import Any

from lsprotocol.types import (
    TEXT_DOCUMENT_COMPLETION,
    TEXT_DOCUMENT_DID_CHANGE,
    TEXT_DOCUMENT_DID_OPEN,
    TEXT_DOCUMENT_DOCUMENT_LINK,
    TEXT_DOCUMENT_FORMATTING,
    TEXT_DOCUMENT_HOVER,
    CompletionItem,
    CompletionItemKind,
    CompletionList,
    CompletionParams,
    DidChangeTextDocumentParams,
    DocumentFormattingParams,
    DocumentLink,
    DocumentLinkParams,
    Hover,
    MarkupContent,
    MarkupKind,
    Position,
    TextDocumentPositionParams,
    TextEdit,
)
from pygls.server import LanguageServer
from tree_sitter_languages import get_parser
from tree_sitter_lsp.diagnose import get_diagnostics
from tree_sitter_lsp.finders import PositionFinder
from tree_sitter_lsp.format import get_text_edits

from .finders import (
    DIAGNOSTICS_FINDER_CLASSES,
    FORMAT_FINDER_CLASSES,
    CSVFinder,
    PackageFinder,
)
from .packages import search_package_document, search_package_names
from .utils import get_filetype, get_schema


class TermuxLanguageServer(LanguageServer):
    r"""Termux language server."""

    def __init__(self, *args: Any) -> None:
        r"""Init.

        :param args:
        :type args: Any
        :rtype: None
        """
        super().__init__(*args)
        self.trees = {}
        self.parser = get_parser("bash")

        @self.feature(TEXT_DOCUMENT_DID_OPEN)
        @self.feature(TEXT_DOCUMENT_DID_CHANGE)
        def did_change(params: DidChangeTextDocumentParams) -> None:
            r"""Did change.

            :param params:
            :type params: DidChangeTextDocumentParams
            :rtype: None
            """
            filetype = get_filetype(params.text_document.uri)
            if filetype == "":
                return None
            document = self.workspace.get_document(params.text_document.uri)
            self.trees[document.uri] = self.parser.parse(
                document.source.encode()
            )
            diagnostics = get_diagnostics(
                document.uri,
                self.trees[document.uri],
                DIAGNOSTICS_FINDER_CLASSES,
                filetype,
            )
            if document.path is not None and filetype == "PKGBUILD":
                from .tools.namcap import namcap

                diagnostics += namcap(document.path, document.source)
            self.publish_diagnostics(params.text_document.uri, diagnostics)

        @self.feature(TEXT_DOCUMENT_FORMATTING)
        def format(params: DocumentFormattingParams) -> list[TextEdit]:
            r"""Format.

            :param params:
            :type params: DocumentFormattingParams
            :rtype: list[TextEdit]
            """
            filetype = get_filetype(params.text_document.uri)
            if filetype == "":
                return []
            document = self.workspace.get_document(params.text_document.uri)
            return get_text_edits(
                document.uri,
                self.trees[document.uri],
                FORMAT_FINDER_CLASSES,
                filetype,
            )

        @self.feature(TEXT_DOCUMENT_DOCUMENT_LINK)
        def document_link(params: DocumentLinkParams) -> list[DocumentLink]:
            r"""Get document links.

            :param params:
            :type params: DocumentLinkParams
            :rtype: list[DocumentLink]
            """
            filetype = get_filetype(params.text_document.uri)
            if filetype == "":
                return []
            document = self.workspace.get_document(params.text_document.uri)
            if filetype in {"build.sh", "subpackage.sh"}:
                return CSVFinder(filetype).get_document_links(
                    document.uri,
                    self.trees[document.uri],
                    "https://github.com/termux/termux-packages/tree/master/packages/{{name}}/build.sh",
                )
            elif filetype in {"PKGBUILD", "install"}:
                return PackageFinder().get_document_links(
                    document.uri,
                    self.trees[document.uri],
                    "https://archlinux.org/packages/{{uni.get_text()}}",
                )
            raise NotImplementedError

        @self.feature(TEXT_DOCUMENT_HOVER)
        def hover(params: TextDocumentPositionParams) -> Hover | None:
            r"""Hover.

            :param params:
            :type params: TextDocumentPositionParams
            :rtype: Hover | None
            """
            filetype = get_filetype(params.text_document.uri)
            if filetype == "":
                return None
            document = self.workspace.get_document(params.text_document.uri)
            uni = PositionFinder(params.position).find(
                document.uri, self.trees[document.uri]
            )
            if uni is None:
                return None
            parent = uni.node.parent
            if parent is None:
                return None
            text = uni.get_text()
            _range = uni.get_range()
            # we only hover variable names and function names
            if not (
                uni.node.type == "variable_name"
                or uni.node.type == "word"
                and parent.type
                in {
                    "function_definition",
                    "command_name",
                }
            ):
                # or package names (for PKGBUILD)
                if parent.type == "array":
                    result = search_package_document(text, filetype)
                    if result is None:
                        return None
                    return Hover(
                        MarkupContent(MarkupKind.Markdown, result), _range
                    )
                return None
            if description := (
                get_schema(filetype)
                .get("properties", {})
                .get(text, {})
                .get("description")
            ):
                return Hover(
                    MarkupContent(MarkupKind.Markdown, description),
                    _range,
                )
            for k, v in (
                get_schema(filetype).get("patternProperties", {}).items()
            ):
                if re.match(k, text):
                    return Hover(
                        MarkupContent(MarkupKind.Markdown, v["description"]),
                        _range,
                    )

        @self.feature(TEXT_DOCUMENT_COMPLETION)
        def completions(params: CompletionParams) -> CompletionList:
            r"""Completions.

            :param params:
            :type params: CompletionParams
            :rtype: CompletionList
            """
            filetype = get_filetype(params.text_document.uri)
            if filetype == "":
                return CompletionList(False, [])
            document = self.workspace.get_document(params.text_document.uri)
            uni = PositionFinder(
                Position(params.position.line, params.position.character - 1)
            ).find(document.uri, self.trees[document.uri])
            if uni is None:
                return CompletionList(False, [])
            parent = uni.node.parent
            if parent is None:
                return CompletionList(False, [])
            text = uni.get_text()
            if parent.type == "array":
                return CompletionList(
                    False,
                    [
                        CompletionItem(
                            k,
                            kind=CompletionItemKind.Module,
                            insert_text=k,
                        )
                        for k in search_package_names(filetype)
                        if k.startswith(text)
                    ],
                )
            schema = get_schema(filetype)
            return CompletionList(
                False,
                [
                    CompletionItem(
                        k,
                        kind=CompletionItemKind.Function
                        if v.get("const") == 0
                        else CompletionItemKind.Field
                        if v.get("type") == "array"
                        else CompletionItemKind.Variable,
                        documentation=MarkupContent(
                            MarkupKind.Markdown, v["description"]
                        ),
                        insert_text=k,
                    )
                    for k, v in (
                        schema.get("properties", {})
                        | {
                            k.lstrip("^").split("(")[0]: v
                            for k, v in schema.get(
                                "patternProperties", {}
                            ).items()
                        }
                    ).items()
                    if k.startswith(text)
                ],
            )
