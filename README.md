# termux-language-server

[![readthedocs](https://shields.io/readthedocs/termux-language-server)](https://termux-language-server.readthedocs.io)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Freed-Wu/termux-language-server/main.svg)](https://results.pre-commit.ci/latest/github/Freed-Wu/termux-language-server/main)
[![github/workflow](https://github.com/Freed-Wu/termux-language-server/actions/workflows/main.yml/badge.svg)](https://github.com/Freed-Wu/termux-language-server/actions)
[![codecov](https://codecov.io/gh/Freed-Wu/termux-language-server/branch/main/graph/badge.svg)](https://codecov.io/gh/Freed-Wu/termux-language-server)
[![DeepSource](https://deepsource.io/gh/Freed-Wu/termux-language-server.svg/?show_trend=true)](https://deepsource.io/gh/Freed-Wu/termux-language-server)

[![github/downloads](https://shields.io/github/downloads/Freed-Wu/termux-language-server/total)](https://github.com/Freed-Wu/termux-language-server/releases)
[![github/downloads/latest](https://shields.io/github/downloads/Freed-Wu/termux-language-server/latest/total)](https://github.com/Freed-Wu/termux-language-server/releases/latest)
[![github/issues](https://shields.io/github/issues/Freed-Wu/termux-language-server)](https://github.com/Freed-Wu/termux-language-server/issues)
[![github/issues-closed](https://shields.io/github/issues-closed/Freed-Wu/termux-language-server)](https://github.com/Freed-Wu/termux-language-server/issues?q=is%3Aissue+is%3Aclosed)
[![github/issues-pr](https://shields.io/github/issues-pr/Freed-Wu/termux-language-server)](https://github.com/Freed-Wu/termux-language-server/pulls)
[![github/issues-pr-closed](https://shields.io/github/issues-pr-closed/Freed-Wu/termux-language-server)](https://github.com/Freed-Wu/termux-language-server/pulls?q=is%3Apr+is%3Aclosed)
[![github/discussions](https://shields.io/github/discussions/Freed-Wu/termux-language-server)](https://github.com/Freed-Wu/termux-language-server/discussions)
[![github/milestones](https://shields.io/github/milestones/all/Freed-Wu/termux-language-server)](https://github.com/Freed-Wu/termux-language-server/milestones)
[![github/forks](https://shields.io/github/forks/Freed-Wu/termux-language-server)](https://github.com/Freed-Wu/termux-language-server/network/members)
[![github/stars](https://shields.io/github/stars/Freed-Wu/termux-language-server)](https://github.com/Freed-Wu/termux-language-server/stargazers)
[![github/watchers](https://shields.io/github/watchers/Freed-Wu/termux-language-server)](https://github.com/Freed-Wu/termux-language-server/watchers)
[![github/contributors](https://shields.io/github/contributors/Freed-Wu/termux-language-server)](https://github.com/Freed-Wu/termux-language-server/graphs/contributors)
[![github/commit-activity](https://shields.io/github/commit-activity/w/Freed-Wu/termux-language-server)](https://github.com/Freed-Wu/termux-language-server/graphs/commit-activity)
[![github/last-commit](https://shields.io/github/last-commit/Freed-Wu/termux-language-server)](https://github.com/Freed-Wu/termux-language-server/commits)
[![github/release-date](https://shields.io/github/release-date/Freed-Wu/termux-language-server)](https://github.com/Freed-Wu/termux-language-server/releases/latest)

[![github/license](https://shields.io/github/license/Freed-Wu/termux-language-server)](https://github.com/Freed-Wu/termux-language-server/blob/main/LICENSE)
[![github/languages](https://shields.io/github/languages/count/Freed-Wu/termux-language-server)](https://github.com/Freed-Wu/termux-language-server)
[![github/languages/top](https://shields.io/github/languages/top/Freed-Wu/termux-language-server)](https://github.com/Freed-Wu/termux-language-server)
[![github/directory-file-count](https://shields.io/github/directory-file-count/Freed-Wu/termux-language-server)](https://github.com/Freed-Wu/termux-language-server)
[![github/code-size](https://shields.io/github/languages/code-size/Freed-Wu/termux-language-server)](https://github.com/Freed-Wu/termux-language-server)
[![github/repo-size](https://shields.io/github/repo-size/Freed-Wu/termux-language-server)](https://github.com/Freed-Wu/termux-language-server)
[![github/v](https://shields.io/github/v/release/Freed-Wu/termux-language-server)](https://github.com/Freed-Wu/termux-language-server)

[![pypi/status](https://shields.io/pypi/status/termux-language-server)](https://pypi.org/project/termux-language-server/#description)
[![pypi/v](https://shields.io/pypi/v/termux-language-server)](https://pypi.org/project/termux-language-server/#history)
[![pypi/downloads](https://shields.io/pypi/dd/termux-language-server)](https://pypi.org/project/termux-language-server/#files)
[![pypi/format](https://shields.io/pypi/format/termux-language-server)](https://pypi.org/project/termux-language-server/#files)
[![pypi/implementation](https://shields.io/pypi/implementation/termux-language-server)](https://pypi.org/project/termux-language-server/#files)
[![pypi/pyversions](https://shields.io/pypi/pyversions/termux-language-server)](https://pypi.org/project/termux-language-server/#files)

Language server for
[termux](https://termux.dev)'s
[`build.sh`](https://github.com/termux/termux-packages/wiki/Creating-new-package)
and
[`*.subpackage.sh`](https://github.com/termux/termux-packages/wiki/Creating-new-package#writing-a-subpackage-script).

`build.sh` is a subtype of bash. See
[bash-language-server](https://github.com/bash-lsp/bash-language-server)
to get support of bash language server.

- [x] document hover
- [x] completion

![document hover](https://github.com/Freed-Wu/pkgbuild-language-server/assets/32936898/61d7f191-4ca2-4790-bcdc-d0c1ceecf430)

![completion](https://github.com/Freed-Wu/pkgbuild-language-server/assets/32936898/6de7967d-878e-4742-a6f3-e3edfaeaa644)

Read
[![readthedocs](https://shields.io/readthedocs/termux-language-server)](https://termux-language-server.readthedocs.io)
to know more.

## Similar Projects

- [pkgbuild-language-server](https://github.com/Freed-Wu/pkgbuild-language-server):
  ArchLinux's `PKGBUILD`.
