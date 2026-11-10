r"""Portage
===========
"""

import re
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path
from types import SimpleNamespace

from jinja2 import Template
from lsp_tree_sitter.completer import PackageSearcher
from platformdirs import user_config_path
from portage.dbapi.porttree import portdbapi
from portage.dep import dep_getkey
from portage.exception import InvalidAtom


def get_template(name: str = "_ebuild.md.jinja") -> Template:
    path = user_config_path("portage") / name
    if not path.exists():
        path = Path(__file__).parent.parent / "assets" / "jinja" / name
    return Template(path.read_text())


@dataclass
class PortageSearcher(PackageSearcher):
    label: str = "package._ebuild"
    texts: tuple[str, ...] = (
        "DEPEND",
        "RDEPEND",
        "BDEPEND",
        "IDEPEND",
        "PDEPEND",
    )
    url_template: str = "https://packages.gentoo.org/packages/{}"
    template: Template = field(default_factory=get_template)
    db: portdbapi = portdbapi()
    executor: ThreadPoolExecutor = ThreadPoolExecutor(max_workers=1)

    @staticmethod
    def get_package_name(name: str) -> str:
        r"""Wrap dep_getkey(), which doesn't support whitespaces and incomplete
        package name, such as dev-lua/LuaBitOp[${LUA_USEDEP}]
        """
        m = re.search(r"\(([^)]*)\)", name)
        name = m.group(1).strip() if m else name.partition("[")[0].strip()
        try:
            return dep_getkey(name)
        except InvalidAtom:
            try:
                return dep_getkey(name + "0")
            except InvalidAtom:
                return name

    def has_package(self, name: str) -> bool:
        return self.db.cp_list(name) != []

    def get_package_url(self, name: str) -> str:
        return self.url_template.format(name)

    def get_package_version(self, name: str) -> str:
        versions: list[str] = self.db.cp_list(name)
        # latest version
        version: str = versions[-1]
        return version.rpartition("-")[-1]

    def get_package_names(self, name: str) -> dict[str, str]:
        return {cp: "" for cp in self.db.cp_all() if cp.startswith(name)}

    def get_package_document(self, name: str) -> str:
        return self.executor.submit(self.render_document, name).result()

    def render_document(self, name: str) -> str:
        cpv = self.get_package_version(name)
        description, homepage, license_, slot, keywords = self.db.aux_get(
            cpv, ["DESCRIPTION", "HOMEPAGE", "LICENSE", "SLOT", "KEYWORDS"]
        )
        version = cpv[len(name) + 1 :]
        pkg = SimpleNamespace(
            description=description,
            version=version,
            slot=slot,
            homepage=homepage,
            license=license_,
            keywords=keywords,
        )
        return self.template.render(pkg=pkg)
