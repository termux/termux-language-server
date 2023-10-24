r"""Utils
=========
"""
from typing import Callable


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
    _paths = {
        k: []
        for k in get_filetype.__annotations__["return"].__args__
        if k != ""
    }
    for path in paths:
        filetype = get_filetype(path)
        for _filetype, filepaths in _paths.items():
            if filetype == _filetype:
                filepaths += [path]
    return _paths
