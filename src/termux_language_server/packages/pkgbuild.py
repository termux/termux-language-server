r"""PKGBUILD packages
=====================
"""

from pathlib import Path

from jinja2 import Template
from platformdirs import user_config_path
from pyalpm import Handle, Package

DB = Handle(".", "/var/lib/pacman").get_localdb()
TEMPLATE_NAME = "template.md.j2"
PATH = user_config_path("pacman") / TEMPLATE_NAME
if not PATH.exists():
    PATH = Path(__file__).parent.parent / "assets" / "jinja2" / TEMPLATE_NAME
TEMPLATE = PATH.read_text()


def render_document(pkg: Package, template: str = TEMPLATE) -> str:
    r"""Render document.

    :param pkg:
    :type pkg: Package
    :param template:
    :type template: str
    :rtype: str
    """
    return Template(template).render(pkg=pkg)


def get_package_document(name: str, template: str = TEMPLATE) -> str:
    r"""Get package document.

    :param name:
    :type name: str
    :param template:
    :type template: str
    :rtype: str
    """
    return render_document(DB.get_pkg(name), template)


def get_package_names(name: str) -> dict[str, str]:
    r"""Get package names.

    :param name:
    :type name: str
    :rtype: dict[str, str]
    """
    return {
        pkg.name: render_document(pkg)
        for pkg in DB.search(name)
        if pkg.name.startswith(name)
    }
