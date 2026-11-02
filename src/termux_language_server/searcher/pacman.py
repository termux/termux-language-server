r"""Pacman
==========
"""

import os
from dataclasses import dataclass, field
from pathlib import Path

from jinja2 import Template
from lsp_tree_sitter.completer import PackageSearcher
from marisa_trie import Trie
from platformdirs import user_cache_dir, user_config_path
from pyalpm import DB, Package
from pycman.config import init_with_config
from tree_sitter import Node


def get_template(name: str = "PKGBUILD.md.jinja") -> Template:
    path = user_config_path("pacman") / name
    if not path.exists():
        path = Path(__file__).parent.parent / "assets" / "jinja" / name
    return Template(path.read_text())


def get_dbs() -> tuple[DB, ...]:
    r"""The local database and the databases of the repositories of
    pacman.conf.
    - Only reading the local database makes the result depend on what is
      installed, e.g. a build dependency of a foreign architecture.
    - A repository which was never synchronized is still unknown.
    """
    try:
        handle = init_with_config("/etc/pacman.conf")
    except FileNotFoundError:
        return ()
    return (handle.get_localdb(), *handle.get_syncdbs())


def get_trie() -> Trie | None:
    path = user_cache_dir("paru", version="packages.aur")
    if not os.path.exists(path):
        return
    with open(path) as f:
        text = f.read()
    return Trie(text.splitlines())


@dataclass
class PacmanSearcher(PackageSearcher):
    label: str = "package.PKGBUILD"
    texts: tuple[str, ...] = (
        "depends",
        "makedepends",
        "optdepends",
        "conflicts",
        "provides",
        "replaces",
    )
    template: Template = field(default_factory=get_template)
    dbs: tuple[DB, ...] = get_dbs()
    trie: Trie | None = field(default_factory=get_trie)

    @staticmethod
    def get_package_name(name: str) -> str:
        r"""`package>=0.0.1` -> `package`.
        - Support the description of an optional dependency:
          `pkgname: Let's ...` -> `pkgname`
        - Handle raw string: `'package'`
        """
        if name.startswith("'") and name.endswith("'"):
            name = name.strip("'")
        for sep in "><=!:":
            name = name.partition(sep)[0]
        return name.strip()

    def __call__(self, node: Node | None) -> bool:
        node = node.parent if node and node.type == "string_content" else node
        return super().__call__(node)

    def get_pkgs(self, name: str) -> list[Package]:
        for db in self.dbs:
            pkg = db.get_pkg(name)
            if pkg:
                return [pkg]
        # virtual packages
        pkgs = []
        for db in self.dbs:
            pkgs += [pkg for pkg in db.search(name) if name in pkg.provides]
        return pkgs

    def has_package(self, name: str) -> bool:
        if self.get_pkgs(name):
            return True
        if self.trie:
            return name in self.trie.keys(name)
        return False

    def get_package_url(self, name: str) -> str:
        r"""TODO: https://packages.msys2.org/base/{name} for mingw_arch"""
        pkgs = self.get_pkgs(name)
        if pkgs:
            name = pkgs[0].name
        if self.trie and name in self.trie.keys(name):
            return f"https://aur.archlinux.org/packages/{name}"
        return f"https://archlinux.org/packages/{name}"

    def get_package_version(self, name: str) -> str:
        if not self.get_pkgs(name):
            return ""
        pkg = self.get_pkgs(name)[0]
        version = pkg.version
        if pkg.name != name:
            version = pkg.name + " " + version
        return version

    def get_package_names(self, name: str) -> dict[str, str]:
        names = {}
        for db in self.dbs:
            for pkg in db.search(name):
                if pkg.name.startswith(name) and pkg.name not in names:
                    names[pkg.name] = self.template.render(pkg=pkg)
        if self.trie:
            for pkg in self.trie.keys(name):
                if pkg not in names:
                    names[pkg] = ""
        return names

    def get_package_document(self, name: str) -> str:
        if not self.get_pkgs(name):
            return ""
        docs = []
        for pkg in self.get_pkgs(name):
            docs += [self.template.render(pkg=pkg)]
        return "\n".join(docs)
