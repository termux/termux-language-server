r"""Utils
=========
"""
from gzip import decompress
from itertools import chain
from urllib import request

from bs4 import BeautifulSoup, FeatureNotFound
from markdown_it import MarkdownIt
from markdown_it.token import Token
from platformdirs import site_data_path, user_data_path
from pygls.uris import uri_scheme
from pypandoc import convert_text


def get_man(filename: str) -> str:
    r"""Get man.

    :param filename:
    :type filename: str
    :rtype: str
    """
    filename += ".5*"
    text = b""
    path = ""
    for path in chain(
        (site_data_path("man") / "man5").glob(filename),
        (user_data_path("man") / "man5").glob(filename),
    ):
        try:
            with open(path, "rb") as f:
                text = f.read()
            break
        except Exception:  # nosec: B112
            continue
    if text == b"":
        raise FileNotFoundError
    _, _, ext = str(path).rpartition(".")
    if ext != "5":
        text = decompress(text)
    return text.decode()


def html2soup(html: str) -> BeautifulSoup:
    r"""Html2soup.

    :param html:
    :type html: str
    :rtype: BeautifulSoup
    """
    try:
        soup = BeautifulSoup(html, "lxml")
    except FeatureNotFound:
        soup = BeautifulSoup(html, "html.parser")
    return soup


def get_soup(uri: str) -> BeautifulSoup:
    r"""Get soup.

    :param uri:
    :type uri: str
    :rtype: BeautifulSoup
    """
    if uri_scheme(uri):
        with request.urlopen(uri) as f:  # nosec: B310
            html = f.read()
    else:
        text = get_man(uri)
        html = convert_text(text, "html", "man")
    return html2soup(html)


def get_md_tokens(filename: str) -> list[Token]:
    r"""Get markdown tokens.

    :param filename:
    :type filename: str
    :rtype: list[Token]
    """
    md = MarkdownIt("commonmark", {})
    text = get_man(filename)
    return md.parse(convert_text(text, "markdown", "man"))
