r"""Pacman
==========
"""

from dataclasses import dataclass, field
from pathlib import Path

from jinja2 import Template
from lsp_tree_sitter.completer import PackageSearcher
from platformdirs import user_config_path
from pyalpm import DB, Handle


def get_template(name: str = "PKGBUILD.md.jinja") -> Template:
    path = user_config_path("pacman") / name
    if not path.exists():
        path = Path(__file__).parent.parent / "assets" / "jinja" / name
    return Template(path.read_text())


@dataclass
class PacmanSearcher(PackageSearcher):
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

    def get_package_names(self, name: str) -> dict[str, str]:
        return {
            pkg.name: self.template.render(pkg=pkg)
            for pkg in DB.search(name)
            if pkg.name.startswith(name)
        }

    def get_package_document(self, name: str) -> str | None:
        pkg = self.db.get_pkg(name)
        if pkg:
            return self.template.render(pkg=pkg)
