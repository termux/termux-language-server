#!/usr/bin/env python
import json

from lsp_tree_sitter.misc import get_soup

SOURCE = "https://github.com/termux/termux-language-server"

filetype = "makepkg.conf"
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
name = ""
for blockquote in get_soup("makepkg.conf").find_all("blockquote"):
    if blockquote.find("p").contents == ["."]:
        break
    p = blockquote.find_previous("p")
    if p.find("strong") is None:
        continue
    if p.text.islower():
        schema["properties"][name]["items"]["enum"] = schema["properties"][
            name
        ]["items"].get("enum", []) + [p.text, f"!{p.text}"]
        continue
    _description = "\n".join(
        content.text.replace("\n", " ")
        for p in blockquote.find_all("p")
        for content in p.contents
    )
    last_name = ""
    example = ""
    text = ""
    name = ""
    for text in [content.text for content in p.contents]:
        # FIXME: typo of makepkg.conf
        if "=" in text or text == "COMPRESSLZO":
            if text == "COMPRESSLZO":
                text += "="
            name = text.split("=")[0]
            if last_name != "":
                description = f"""```sh
{example}
```
{_description}"""
                schema["properties"][last_name] = {
                    "description": description,
                    "type": "array" if "(" in example else "string",
                }
                if schema["properties"][last_name]["type"] == "array":
                    schema["properties"][last_name] |= {
                        "items": {"type": "string"},
                        "uniqueItems": True,
                    }
                example = ""
            last_name = name
        example += text.replace("\n", " ")
    else:
        description = f"""```sh
{example}
```
{_description}"""
        schema["properties"][name] = {
            "description": description,
            "type": "array" if "(" in example else "string",
        }
        if schema["properties"][last_name]["type"] == "array":
            schema["properties"][last_name] |= {
                "items": {"type": "string"},
                "uniqueItems": True,
            }
print(json.dumps(schema, indent=2))
