r"""Licenses
============
"""

from license_expression import get_license_index

LICENSES = [
    i["spdx_license_key"]
    for i in get_license_index()
    if i.get("spdx_license_key")
    and not i["spdx_license_key"].startswith("LicenseRef-scancode-")
]
ATOM = f"({'|'.join(LICENSES)})"
