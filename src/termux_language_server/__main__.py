r"""This module can be called by
`python -m <https://docs.python.org/3/library/__main__.html>`_.
"""
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from contextlib import suppress
from datetime import datetime

from . import __name__ as NAME
from . import __version__

NAME = NAME.replace("_", "-")
VERSION = rf"""{NAME} {__version__}
Copyright (C) {datetime.now().year}
Written by Wu Zhenyu
"""
EPILOG = """
Report bugs to <wuzhenyu@ustc.edu>.
"""


def get_parser():
    r"""Get a parser for unit test."""
    parser = ArgumentParser(
        epilog=EPILOG,
        formatter_class=RawDescriptionHelpFormatter,
    )
    with suppress(ImportError):
        import shtab

        shtab.add_argument_to(parser)
    parser.add_argument("--version", version=VERSION, action="version")
    parser.add_argument(
        "--check",
        nargs="*",
        default=[],
        help="check file's errors and warnings",
    )
    parser.add_argument(
        "--format",
        nargs="*",
        default=[],
        help="format files",
    )
    parser.add_argument(
        "--color",
        choices=["auto", "always", "never"],
        default="auto",
        help="when to display color",
    )
    return parser


def main():
    r"""Parse arguments and provide shell completions."""
    parser = get_parser()
    args = parser.parse_args()

    from .parser import parse
    from .utils import check, format

    format(args.format, parse)
    result = check(args.check, parse, args.color)
    if args.format or args.check:
        exit(result)

    from .server import TermuxLanguageServer

    TermuxLanguageServer(NAME, __version__).start_io()


if __name__ == "__main__":
    main()
