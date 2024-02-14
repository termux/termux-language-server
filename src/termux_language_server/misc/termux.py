r"""Termux
==========
"""

from typing import Any

from tree_sitter_lsp.misc import get_soup

from .. import CSV
from .._metainfo import SOURCE, project
from .licenses import ATOM

URIS = {
    "variable": "https://github.com/termux/termux-packages/wiki/Creating-new-package",
    "function": "https://github.com/termux/termux-packages/wiki/Building-packages",
    "update": "https://github.com/termux/termux-packages/wiki/Auto-updating-packages",
}


def init_schema() -> dict[str, dict[str, Any]]:
    r"""Init schema.

    :rtype: dict[str, dict[str, Any]]
    """
    schemas = {}
    for filetype in {"build.sh", "subpackage.sh"}:
        schemas[filetype] = {
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
            # required variables
            "required": [],
            # all variables and all overridable functions
            "properties": {},
            "propertyNames": {
                # not overridable functions
                # for subpackage.sh, disable all functions
                "not": {"anyOf": []}
            },
        }

    soup = get_soup(URIS["variable"])
    tables = soup.find_all("table")
    for tr in tables[0].find_all("tr")[1:]:
        tds = tr.find_all("td")
        name = tds[1].text
        is_required = tds[2].text == "yes"
        description = tds[3].text.strip()
        if is_required:
            schemas["build.sh"]["required"] += [name]
        schemas["build.sh"]["properties"][name] = {
            "type": "string",
            "description": description,
        }
        if description.endswith("Default is true."):
            schemas["build.sh"]["properties"][name]["default"] = "true"
            schemas["build.sh"]["properties"][name]["enum"] = ["true", "false"]
        if description.endswith("Default is false."):
            schemas["build.sh"]["properties"][name]["default"] = "false"
            schemas["build.sh"]["properties"][name]["enum"] = ["true", "false"]
        if description.startswith("Comma-separated list of "):
            schemas["build.sh"]["properties"][name]["pattern"] = CSV
    for tr in tables[2].find_all("tr")[1:]:
        tds = tr.find_all("td")
        name = tds[1].text
        is_required = tds[2].text == "yes"
        description = tds[3].text.strip()
        if is_required:
            schemas["subpackage.sh"]["required"] += [name]
        schemas["subpackage.sh"]["properties"][name] = {
            "type": "string",
            "description": description,
        }
        if description.endswith("Default is true."):
            schemas["subpackage.sh"]["properties"][name]["default"] = "true"
            schemas["subpackage.sh"]["properties"][name]["enum"] = [
                "true",
                "false",
            ]
        if description.endswith("Default is false."):
            schemas["subpackage.sh"]["properties"][name]["default"] = "false"
            schemas["subpackage.sh"]["properties"][name]["enum"] = [
                "true",
                "false",
            ]
        if description.startswith("Comma-separated list of "):
            schemas["subpackage.sh"]["properties"][name]["pattern"] = CSV
    for li in soup.find_all("ul")[-2].find_all("li"):
        name = li.find("code").text
        description = (
            li.text.partition("-")[2].strip().replace("\n", " ").strip()
        )
        obj = {
            "const": name,
            "description": description,
        }
        schemas["build.sh"]["propertyNames"]["not"]["anyOf"] += [obj]
        schemas["subpackage.sh"]["propertyNames"]["not"]["anyOf"] += [obj]

    variable_table, function_table = get_soup(URIS["update"]).find_all("table")
    for tr in variable_table.find_all("tr")[1:]:
        tds = tr.find_all("td")
        name = tds[1].text
        is_required = tds[2].text == "yes"
        description = tds[3].text.strip()
        if is_required:
            schemas["build.sh"]["required"] += [name]
        schemas["build.sh"]["properties"][name] = {
            "type": "string",
            "description": description,
        }
        if description.startswith("Comma-separated list of "):
            schemas["build.sh"]["properties"][name]["pattern"] = CSV

    for tr in (
        get_soup(URIS["function"]).find_all("tr")[1:]
        + function_table.find_all("tr")[1:]
    ):
        tds = tr.find_all("td")
        name = tds[1].text
        # NOTE: capital
        # use `!=  "no"` to allow some conditional yes
        is_overrideable = tds[2].text.lower() != "no"
        description = tds[3].text.strip()
        if is_overrideable:
            schemas["build.sh"]["properties"][name] = {
                "description": description,
                "const": 0,
            }
        else:
            obj = {
                "const": name,
                "description": description,
            }
            schemas["build.sh"]["propertyNames"]["not"]["anyOf"] += [obj]

    schemas["build.sh"]["properties"]["TERMUX_PKG_HOMEPAGE"][
        "format"
    ] = schemas["build.sh"]["properties"]["TERMUX_PKG_SRCURL"]["format"] = (
        "uri"
    )
    schemas["build.sh"]["properties"]["TERMUX_PKG_MAINTAINER"]["default"] = (
        "@termux"
    )
    schemas["build.sh"]["properties"]["TERMUX_PKG_UPDATE_METHOD"]["enum"] = [
        "github",
        "gitlab",
        "repology",
    ]
    schemas["build.sh"]["properties"]["TERMUX_GITLAB_API_HOST"]["default"] = (
        "gitlab.com"
    )
    schemas["build.sh"]["properties"]["TERMUX_GITLAB_API_HOST"]["format"] = (
        "hostname"
    )
    schemas["build.sh"]["properties"]["TERMUX_PKG_UPDATE_VERSION_REGEXP"][
        "format"
    ] = "regex"
    schemas["build.sh"]["properties"]["TERMUX_PKG_LICENSE"]["pattern"] = (
        rf"{ATOM}(,{ATOM})*"
    )
    return schemas
