r"""Documents
=============
"""
import json
import os
from typing import Literal

from platformdirs import user_cache_dir


def get_document(
    method: Literal["builtin", "cache", "web"] = "builtin"
) -> tuple[
    dict[str, tuple[str, str]], dict[str, set[str]], dict[str, set[str]]
]:
    r"""Get document. ``builtin`` will use builtin termux.json. ``cache``
    will generate a cache from
    `<https://github.com/termux/termux-packages/wiki/Creating-new-package>`_. ``web`` is same as
    ``cache`` except it doesn't generate cache. We use ``builtin`` as default.
    If you want to get the latest result from
    `<https://github.com/termux/termux-packages/wiki/Creating-new-package>`_, you need to
    install `beautifulsoup4 <https://pypi.org/project/beautifulsoup4>` by
    ``pip install 'termux-language-server[web]'``.

    :param method:
    :type method: Literal["builtin", "cache", "web"]
    :rtype: tuple[dict[str, tuple[str, str]], dict[str, set[str]], dict[str, set[str]]]
    """
    if method == "builtin":
        file = os.path.join(
            os.path.join(
                os.path.join(
                    os.path.dirname(os.path.dirname(__file__)), "assets"
                ),
                "json",
            ),
            "termux.json",
        )
        with open(file, "r") as f:
            document = json.load(f)
    elif method == "cache":
        from .builtin import init_document

        if not os.path.exists(user_cache_dir("termux.json")):
            document = init_document()
            with open(user_cache_dir("termux.json"), "w") as f:
                json.dump(document, f)
        else:
            with open(user_cache_dir("termux.json"), "r") as f:
                document = json.load(f)
    else:
        from .builtin import init_document

        document = init_document()
    return (
        document[0],
        {k: set(v) for k, v in document[1].items()},
        {k: set(v) for k, v in document[2].items()},
    )


def get_filetype(uri: str) -> Literal["build.sh", "subpackage.sh", ""]:
    r"""Get filetype.

    :param uri:
    :type uri: str
    :rtype: Literal["build.sh", "subpackage.sh", ""]
    """
    if os.path.basename(uri) == "build.sh":
        return "build.sh"
    if os.path.basename(uri).endswith(".subpackage.sh"):
        return "subpackage.sh"
    return ""
