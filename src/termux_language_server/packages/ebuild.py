r"""Ebuild packages
==================
"""

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from types import SimpleNamespace

from jinja2 import Template
from platformdirs import user_config_path
from portage import db, root

PORTTREE = db[root]["porttree"].dbapi
_ALL_PACKAGES = PORTTREE.cp_all()
_EXECUTOR = ThreadPoolExecutor(max_workers=1)
TEMPLATE_NAME = "ebuild.md.j2"
PATH = user_config_path("portage") / TEMPLATE_NAME
if not PATH.exists():
    PATH = Path(__file__).parent.parent / "assets" / "jinja2" / TEMPLATE_NAME
TEMPLATE = PATH.read_text()


def _render_document(cp: str, template: str = TEMPLATE) -> str:
    r"""Render document.

    :param cp:
    :type cp: str
    :param template:
    :type template: str
    :rtype: str
    """
    versions = PORTTREE.cp_list(cp)
    if not versions:
        return ""
    cpv = versions[-1]
    description, homepage, license_, slot, keywords = PORTTREE.aux_get(
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
    return Template(template).render(pkg=pkg)


def get_package_document(name: str, template: str = TEMPLATE) -> str:
    r"""Get package document.

    :param name:
    :type name: str
    :param template:
    :type template: str
    :rtype: str
    """
    return _EXECUTOR.submit(_render_document, name, template).result()


def get_package_names(name: str) -> dict[str, str]:
    r"""Get package names.

    :param name:
    :type name: str
    :rtype: dict[str, str]
    """
    return {cp: "" for cp in _ALL_PACKAGES if cp.startswith(name)}
