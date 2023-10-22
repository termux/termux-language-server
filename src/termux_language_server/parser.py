r"""Parser
==========
"""
import os
from glob import glob

from platformdirs import user_data_path
from tree_sitter import Language, Parser, Tree

LIBS = glob(
    os.path.join(
        os.path.join(os.path.join(os.path.dirname(__file__), "data"), "lib"),
        "*",
    )
)
if len(LIBS) > 0:
    LIB = LIBS[0]
else:
    # https://github.com/nvim-treesitter/nvim-treesitter/issues/5493
    LIB = str(
        next(
            (
                user_data_path("nvim")
                / "repos"
                / "github.com"
                / "nvim-treesitter"
                / "nvim-treesitter"
                / "parser"
            ).glob("bash.*")
        )
    )
PARSER = Parser()
PARSER.set_language(Language(LIB, "bash"))


def parse(source: bytes) -> Tree:
    r"""Parse.

    :param source:
    :type source: bytes
    :rtype: Tree
    """
    return PARSER.parse(source)
