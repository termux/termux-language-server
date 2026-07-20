#!/usr/bin/env python
from lsp_tree_sitter.misc import get_soup

SOURCE = "https://github.com/termux/termux-language-server"

filetype = "color.map"
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
dl = get_soup("color.map").find_all("dl")[1]
for dt, dd in zip(dl.find_all("dt"), dl.find_all("dd"), strict=False):
    name = dt.text.split()[0]
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
print(schema)
