r"""PKGBUILD packages
=====================
"""
from pathlib import Path

from jinja2 import Template
from platformdirs import user_config_path

try:
    from pyalpm import Handle

    DB = Handle(".", "/var/lib/pacman").get_localdb()
except ImportError:
    from argparse import Namespace

    DB = Namespace(pkgcache=[])
TEMPLATE_NAME = "template.md.j2"
PATH = user_config_path("pacman") / TEMPLATE_NAME
if not PATH.exists():
    PATH = Path(__file__).parent.parent / "assets" / "jinja2" / TEMPLATE_NAME
TEMPLATE = PATH.read_text()


def get_package_document(name: str, template: str = TEMPLATE) -> str:
    r"""Get package document.

    :param name:
    :type name: str
    :param template:
    :type template: str
    :rtype: str
    """
    for pkg in DB.pkgcache:
        if pkg.name == name:
            return Template(template).render(pkg=pkg)
    return ""


def get_package_names() -> list[str]:
    r"""Get package names.

    :rtype: list[str]
    """
    return [pkg.name for pkg in DB.pkgcache]
