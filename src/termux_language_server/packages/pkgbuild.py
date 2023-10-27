r"""PKGBUILD packages
=====================
"""
from pathlib import Path

from jinja2 import Template
from platformdirs import user_config_path
from pyalpm import Handle

DB = Handle(".", "/var/lib/pacman").get_localdb()
TEMPLATE_NAME = "template.md.j2"
PATH = user_config_path("pacman") / TEMPLATE_NAME
if not PATH.exists():
    PATH = Path(__file__).parent.parent / "assets" / "jinja2" / TEMPLATE_NAME
TEMPLATE = PATH.read_text()


def get_package_document(name: str, template: str | None = TEMPLATE) -> str:
    r"""Get package document.

    :param name:
    :type name: str
    :param template: return description when template is None, which is faster.
    :type template: str | None
    :rtype: str
    """
    if template is None:
        return DB.get_pkg(name).desc
    return Template(template).render(pkg=DB.get_pkg(name))


def get_package_names() -> dict[str, str]:
    r"""Get package names.

    :rtype: dict[str, str]
    """
    return {
        pkg.name: get_package_document(pkg.name, None) for pkg in DB.pkgcache
    }
