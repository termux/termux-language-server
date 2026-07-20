r"""This module can be called by
`python -m <https://docs.python.org/3/library/__main__.html>`_.
"""

from lsp_tree_sitter.__main__ import get_parser

from . import __version__


def main():
    parser = get_parser(__version__)
    args = parser.parse_args()

    from .server import TermuxLanguageServer as Server

    server = Server(version=__version__)
    server.run(args)


if __name__ == "__main__":
    main()
