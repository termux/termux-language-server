r"""Utils
=========

Some common functions used by formatters and linters.
"""
from typing import Callable

from . import Finder


def get_paths(
    paths: list[str], get_filetype: Callable[[str], str]
) -> dict[str, list[str]]:
    r"""Get paths.

    :param paths:
    :type paths: list[str]
    :param get_filetype:
    :type get_filetype: Callable[[str], str]
    :rtype: dict[str, list[str]]
    """
    filetype_paths = {
        k: []
        for k in get_filetype.__annotations__["return"].__args__
        if k != ""
    }
    for path in paths:
        filetype = get_filetype(path)
        for _filetype, filepaths in filetype_paths.items():
            if filetype == _filetype:
                filepaths += [path]
    return filetype_paths


def get_finders(
    classes: list[type[Finder]] | None = None,
) -> tuple[list[Finder], list[type[Finder]]]:
    r"""Get finders.

    :param classes:
    :type classes: list[type[Finder]] | None
    :rtype: tuple[list[Finder], list[type[Finder]]]
    """
    if classes is None:
        from .finders import ErrorFinder, MissingFinder

        classes = [ErrorFinder, MissingFinder]

    finders = []
    finder_classes = []
    for cls in classes:
        if cls.__init__.__annotations__.get("filetype"):
            finder_classes += [cls]
        else:
            finders += [cls()]
    return finders, finder_classes
