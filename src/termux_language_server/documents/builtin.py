r"""Builtin
===========
"""
from copy import deepcopy
from urllib import request

from bs4 import BeautifulSoup, FeatureNotFound

URIS = {
    "variable": "https://github.com/termux/termux-packages/wiki/Creating-new-package",
    "function": "https://github.com/termux/termux-packages/wiki/Building-packages",
    "update": "https://github.com/termux/termux-packages/wiki/Auto-updating-packages",
}


def get_soup(uri: str) -> BeautifulSoup:
    r"""Get soup.

    :param uri:
    :type uri: str
    :rtype: BeautifulSoup
    """
    with request.urlopen(uri) as f:  # nosec: B310
        html = f.read()

    try:
        soup = BeautifulSoup(html, "lxml")
    except FeatureNotFound:
        soup = BeautifulSoup(html, "html.parser")
    return soup


def init_document() -> (
    tuple[
        dict[str, tuple[str, str]], dict[str, list[str]], dict[str, list[str]]
    ]
):
    r"""Init document.

    :rtype: (
        tuple[dict[str, tuple[str, str]], dict[str, list[str]], dict[str, list[str]]]
    )
    """
    items = {}
    required = {"build.sh": [], "subpackage.sh": []}
    csvs = deepcopy(required)
    variable_table, function_table = get_soup(URIS["update"]).find_all("table")
    for tr in (
        get_soup(URIS["function"]).find_all("tr")[1:]
        + function_table.find_all("tr")[1:]
    ):
        tds = tr.find_all("td")
        # overridable means `termux_step_configure() { ... }`
        items[tds[1].text + ("()" if tds[2].text == "yes" else "")] = (
            tds[3].text,
            "",
        )
    soup = get_soup(URIS["variable"])
    tables = soup.find_all("table")
    for tr in tables[0].find_all("tr")[1:]:
        tds = tr.find_all("td")
        if tds[2].text == "yes":
            required["build.sh"] += [tds[1].text]
        if tds[3].text.startswith("Comma-separated list of "):
            csvs["build.sh"] += [tds[1].text]
        items[tds[1].text] = (
            tds[3].text,
            "build.sh",
        )
    for tr in tables[2].find_all("tr")[1:]:
        tds = tr.find_all("td")
        if tds[2].text == "yes":
            required["subpackage.sh"] += [tds[1].text]
        if tds[3].text.startswith("Comma-separated list of "):
            csvs["subpackage.sh"] += [tds[1].text]
        items[tds[1].text] = (
            tds[3].text,
            "subpackage.sh",
        )
    for tr in variable_table.find_all("tr")[1:]:
        tds = tr.find_all("td")
        if tds[2].text == "yes":
            required["build.sh"] += [tds[1].text]
            required["subpackage.sh"] += [tds[1].text]
        if tds[3].text.startswith("Comma-separated list of "):
            csvs["build.sh"] += [tds[1].text]
            csvs["subpackage.sh"] += [tds[1].text]
        items[tds[1].text] = (
            tds[3].text,
            "",
        )
    for li in soup.find_all("ul")[-2].find_all("li"):
        items[li.find("code").text] = (
            li.text.partition("-")[2].strip().replace("\n", " "),
            "",
        )
    return items, required, csvs
