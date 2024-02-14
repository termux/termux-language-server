r"""Portage's make.conf
=======================
"""

from typing import Any

from tree_sitter_lsp.misc import get_soup

from .._metainfo import SOURCE, project


def init_schema() -> dict[str, dict[str, Any]]:
    r"""Init schema.

    :rtype: dict[str, dict[str, Any]]
    """
    filetype = "make.conf"
    schema = {
        "$id": (
            f"{SOURCE}/blob/main/"
            "src/termux_language_server/assets/json/{filetype}.json"
        ),
        "$schema": "http://json-schema.org/draft-07/schema#",
        "$comment": (
            "Don't edit this file directly! It is generated by "
            f"`{project} --generate-schema={filetype}`."
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
    return {filetype: schema}
