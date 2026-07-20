r"""Portage
===========
"""

from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path
from types import SimpleNamespace

from jinja2 import Template
from lsp_tree_sitter.completer import PackageSearcher
from platformdirs import user_config_path
from portage import db, root
from portage.dbapi.porttree import portdbapi


def get_template(name: str = "_ebuild.md.jinja") -> Template:
    path = user_config_path("portage") / name
    if not path.exists():
        path = Path(__file__).parent.parent / "assets" / "jinja" / name
    return Template(path.read_text())


@dataclass
class PortageSearcher(PackageSearcher):
    texts: tuple[str, ...] = (
        "DEPEND",
        "RDEPEND",
        "BDEPEND",
        "IDEPEND",
        "PDEPEND",
    )
    template: Template = field(default_factory=get_template)
    db: portdbapi = field(default_factory=lambda: db[root]["porttree"].dbapi)
    executor: ThreadPoolExecutor = ThreadPoolExecutor(max_workers=1)

    def get_package_names(self, name: str) -> dict[str, str]:
        return {cp: "" for cp in self.db.cp_all() if cp.startswith(name)}

    def get_package_document(self, name: str) -> str:
        return self.executor.submit(self.render_document, name).result()

    def render_document(self, cp: str) -> str:
        versions = self.db.cp_list(cp)
        if not versions:
            return ""
        cpv = versions[-1]
        description, homepage, license_, slot, keywords = self.db.aux_get(
            cpv, ["DESCRIPTION", "HOMEPAGE", "LICENSE", "SLOT", "KEYWORDS"]
        )
        version = cpv[len(cp) + 1 :]
        pkg = SimpleNamespace(
            description=description,
            version=version,
            slot=slot,
            homepage=homepage,
            license=license_,
            keywords=keywords,
        )
        return self.template.render(pkg=pkg)
