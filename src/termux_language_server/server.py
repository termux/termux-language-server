r"""Server
==========
"""
from typing import Any

from lsprotocol.types import (
    INITIALIZE,
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
    InitializeParams,
    MarkupContent,
    MarkupKind,
    Position,
    TextDocumentPositionParams,
    TextEdit,
)
from pygls.server import LanguageServer

from .documents import get_document, get_filetype
from .finders import (
    CSVFinder,
    InvalidKeywordFinder,
    RequiredKeywordFinder,
    UnsortedCSVFinder,
    UnsortedKeywordFinder,
)
from .parser import parse
from .tree_sitter_lsp.diagnose import get_diagnostics
from .tree_sitter_lsp.finders import PositionFinder
from .tree_sitter_lsp.format import get_text_edits
from .utils import DIAGNOSTICS_FINDERS, get_keywords


class TermuxLanguageServer(LanguageServer):
    r"""Termux language server."""

    def __init__(self, *args: Any) -> None:
        r"""Init.

        :param args:
        :type args: Any
        :rtype: None
        """
        super().__init__(*args)
        self.document = {}
        self.keywords = {}
        self.required = {}
        self.csvs = {}
        self.trees = {}

        @self.feature(INITIALIZE)
        def initialize(params: InitializeParams) -> None:
            r"""Initialize.

            :param params:
            :type params: InitializeParams
            :rtype: None
            """
            opts = params.initialization_options
            method = getattr(opts, "method", "builtin")
            self.document, self.required, self.csvs = get_document(method)  # type: ignore
            self.keywords = get_keywords(self.document)

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
            self.trees[document.uri] = parse(document.source.encode())
            diagnostics = get_diagnostics(
                DIAGNOSTICS_FINDERS
                + [
                    RequiredKeywordFinder(self.required[filetype]),
                    InvalidKeywordFinder(set(self.keywords[filetype])),
                    UnsortedKeywordFinder(self.keywords[filetype]),
                    UnsortedCSVFinder(self.csvs[filetype]),
                ],
                document.uri,
                self.trees[document.uri],
            )
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
                [
                    UnsortedKeywordFinder(self.keywords[filetype]),
                    UnsortedCSVFinder(self.csvs[filetype]),
                ],
                document.uri,
                self.trees[document.uri],
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
            return CSVFinder(self.csvs[filetype]).get_document_links(
                document.uri,
                self.trees[document.uri],
                "https://github.com/termux/termux-packages/tree/master/packages/{{name}}/build.sh",
            )

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
            text = uni.get_text()
            _range = uni.get_range()
            parent = uni.node.parent
            if parent is None:
                return None
            if (
                uni.node.type == "variable_name"
                and text.isupper()
                or uni.node.type == "word"
                and parent.type
                in {
                    "function_definition",
                    "command_name",
                }
                and text.islower()
            ):
                return None
            result, _filetype = self.document.get(text, ["", ""])
            if result == "" or _filetype != filetype:
                return None
            return Hover(
                MarkupContent(MarkupKind.PlainText, result),
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
            text = uni.get_text()
            # v[1] can be "", which both build.sh and subpackage.sh need
            return CompletionList(
                False,
                [
                    CompletionItem(
                        k,
                        kind=CompletionItemKind.Variable
                        if k.isupper()
                        else CompletionItemKind.Function,
                        documentation=v[0],
                        insert_text=k,
                    )
                    for k, v in self.document.items()
                    if k.startswith(text) and v[1] in filetype
                ],
            )
