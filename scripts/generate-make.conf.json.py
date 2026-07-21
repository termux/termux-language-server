#!/usr/bin/env python
import json

from lsp_tree_sitter.misc import get_soup

SOURCE = "https://github.com/termux/termux-language-server"


filetype = "make.conf"
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
    "properties": {},
}
for dl in get_soup("make.conf").find_all("dl")[:-2]:
    for dt, dd in zip(dl.find_all("dt"), dl.find_all("dd"), strict=False):
        if dt.strong is None:
            continue
        name = dt.strong.text.split()[0]
        if not name.isupper():
            continue
        description = dd.text.replace("\n", " ").strip()
        example = dt.text.replace("\n", " ")
        if name != example:
            description = f"""```sh
{example}
```
{description}"""
        schema["properties"][name] = {
            "description": description,
            "type": "string",
        }
print(json.dumps(schema, indent=2))
