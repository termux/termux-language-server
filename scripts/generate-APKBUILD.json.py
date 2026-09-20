#!/usr/bin/env python
import json

from lsp_tree_sitter.misc import get_md_tokens
from markdown_it.token import Token

SOURCE = "https://github.com/termux/termux-language-server"


def get_content(tokens: list[Token]) -> str:
    r"""Get content.

    :param tokens:
    :type tokens: list[Token]
    :rtype: str
    """
    return "\n".join([
        token.content.replace("\n", " ") for token in tokens if token.content
    ])


filetype = "APKBUILD"
schema = {
    "$id": (
        f"{SOURCE}/blob/main/"
        f"src/termux_language_server/assets/json/{filetype}.json"
    ),
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$comment": (
        "Don't edit this file directly! It is generated automatically."
    ),
    "type": "object",
    "required": [],
    "properties": {},
}

tokens = get_md_tokens("APKBUILD")
section_indices = [
    index
    for index, token in enumerate(tokens)
    if (
        token.content.endswith("Variables")
        or token.content.endswith("Functions")
        or token.content.endswith("Scripts")
    )
    and token.level == 1
]
indices = [
    index
    for index, token in enumerate(tokens)
    if token.content.startswith("**")
    and token.content.endswith("**")
    and token.level == 1
]
blockquote_close_indices = [
    index
    for index, token in enumerate(tokens)
    if token.type == "blockquote_close"
]
close_indices = [
    min([
        blockquote_close_index
        for blockquote_close_index in blockquote_close_indices
        if blockquote_close_index > index
    ])
    for index in indices
]
for index, close_index in zip(indices, close_indices, strict=False):
    children = tokens[index].children
    if children is None:
        continue
    words = [child.rstrip(",") for child in children[2].content.split()]
    names = [words[0]]
    section_index = section_indices[0]
    for i in section_indices:
        if i < index:
            section_index = i
        else:
            break
    section = tokens[section_index].content
    kind = section.split()[-1]
    if kind == "Scripts":
        continue
    for name in names:
        description = get_content(tokens[index + 1 : close_index])
        schema["properties"][name] = {"description": description}
        if kind == "Variables":
            schema["properties"][name]["type"] = "string"
            if section.split()[0] == "Required":
                schema["required"] += [name]
        elif kind == "Functions":
            schema["properties"][name]["const"] = 0
schema["properties"]["url"]["format"] = "uri"

print(json.dumps(schema, indent=2))
