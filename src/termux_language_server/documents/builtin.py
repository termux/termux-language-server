r"""Builtin
===========
"""
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


def init_document() -> dict[str, tuple[str, str]]:
    r"""Init document.

    :rtype: dict[str, tuple[str, str]]
    """
    items = {}
    variable_table, function_table = get_soup(URIS["update"]).findAll("table")
    for tr in (
        get_soup(URIS["function"]).findAll("tr")[1:]
        + function_table.findAll("tr")[1:]
    ):
        tds = tr.findAll("td")
        # overridable means `termux_step_configure() { ... }`
        items[tds[1].text + ("()" if tds[2].text == "yes" else "")] = (
            tds[3].text,
            "",
        )
    soup = get_soup(URIS["variable"])
    tables = soup.findAll("table")
    for tr in tables[0].findAll("tr")[1:]:
        tds = tr.findAll("td")
        items[tds[1].text] = (
            ("Required\n" if tds[2].text == "yes" else "") + tds[3].text,
            "build.sh",
        )
    for tr in tables[2].findAll("tr")[1:]:
        tds = tr.findAll("td")
        items[tds[1].text] = (
            ("Required\n" if tds[2].text == "yes" else "") + tds[3].text,
            "subpackage.sh",
        )
    for tr in variable_table.findAll("tr")[1:]:
        tds = tr.findAll("td")
        items[tds[1].text] = (
            ("Required\n" if tds[2].text == "yes" else "") + tds[3].text,
            "",
        )
    for li in soup.findAll("ul")[-2].findAll("li"):
        items[li.find("code").text] = (
            li.text.partition("-")[2].strip().replace("\n", " "),
            "",
        )
    return items
