r"""Complete
============
"""
import os
from glob import glob
from pathlib import Path

from lsprotocol.types import CompletionItem, CompletionItemKind, CompletionList

from . import UNI


def get_completion_list_by_uri(
    uri: str, text: str = "", expr: str = "*"
) -> CompletionList:
    r"""Get completion list by uri.

    :param uri:
    :type uri: str
    :param text:
    :type text: str
    :param expr:
    :type expr: str
    :rtype: CompletionList
    """
    dirname = os.path.dirname(UNI.uri2path(uri))
    return CompletionList(
        False,
        [
            CompletionItem(
                x.rpartition(dirname + os.path.sep)[-1],
                kind=CompletionItemKind.File
                if os.path.isfile(x)
                else CompletionItemKind.Folder,
                documentation=Path(x).read_text()
                if os.path.isfile(x)
                else "\n".join(os.listdir(x)),
                insert_text=x.rpartition(dirname + os.path.sep)[-1],
            )
            for x in [
                file + ("" if os.path.isfile(file) else os.path.sep)
                for file in glob(
                    os.path.join(dirname, text + f"**{os.path.sep}" + expr),
                    recursive=True,
                )
            ]
        ],
    )
