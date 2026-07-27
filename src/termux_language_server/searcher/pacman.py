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
from pyalpm import DB, Handle, Package
from tree_sitter import Node


def get_template(name: str = "PKGBUILD.md.jinja") -> Template:
    path = user_config_path("pacman") / name
    if not path.exists():
        path = Path(__file__).parent.parent / "assets" / "jinja" / name
    return Template(path.read_text())


def get_trie() -> Trie | None:
    path = os.path.join(user_cache_dir("paru"), "packages.aur")
    if not os.path.exists(path):
        return
    with open(path) as f:
        lines = f.readlines()
    return Trie(lines)


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
    db: DB = field(
        default_factory=lambda: Handle(".", "/var/lib/pacman").get_localdb()
    )
    trie: Trie | None = field(default_factory=get_trie)

    def __call__(self, node: Node | None) -> bool:
        node = node.parent if node and node.type == "string_content" else node
        return super().__call__(node)

    def get_pkgs(self, name: str) -> list[Package]:
        pkg = self.db.get_pkg(name)
        if pkg:
            return [pkg]
        # virtual packages
        pkgs = []
        for pkg in self.db.search(name):
            if name in pkg.provides:
                pkgs += [pkg]
        return pkgs

    def has_package(self, name: str) -> bool:
        if self.get_pkgs(name):
            return True
        if self.trie:
            return name in self.trie.keys(name)
        return False

    def get_package_url(self, name: str) -> str:
        if self.get_pkgs(name):
            return f"https://archlinux.org/packages/{name}"
        return f"https://aur.archlinux.org/packages/{name}"

    def get_package_version(self, name: str) -> str:
        if not self.get_pkgs(name):
            return ""
        pkg = self.get_pkgs(name)[0]
        version = pkg.version
        if pkg.name != name:
            version = pkg.name + " " + version
        return version

    def get_package_names(self, name: str) -> dict[str, str]:
        names = {
            pkg.name: self.template.render(pkg=pkg)
            for pkg in self.db.search(name)
            if pkg.name.startswith(name)
        }
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
