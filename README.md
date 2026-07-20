# termux-language-server

[![readthedocs](https://shields.io/readthedocs/termux-language-server)](https://termux-language-server.readthedocs.io)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/termux/termux-language-server/main.svg)](https://results.pre-commit.ci/latest/github/termux/termux-language-server/main)
[![github/workflow](https://github.com/termux/termux-language-server/actions/workflows/main.yml/badge.svg)](https://github.com/termux/termux-language-server/actions)
[![codecov](https://codecov.io/gh/termux/termux-language-server/branch/main/graph/badge.svg)](https://codecov.io/gh/termux/termux-language-server)
[![DeepSource](https://deepsource.io/gh/termux/termux-language-server.svg/?show_trend=true)](https://deepsource.io/gh/termux/termux-language-server)

[![github/downloads](https://shields.io/github/downloads/termux/termux-language-server/total)](https://github.com/termux/termux-language-server/releases)
[![github/downloads/latest](https://shields.io/github/downloads/termux/termux-language-server/latest/total)](https://github.com/termux/termux-language-server/releases/latest)
[![github/issues](https://shields.io/github/issues/termux/termux-language-server)](https://github.com/termux/termux-language-server/issues)
[![github/issues-closed](https://shields.io/github/issues-closed/termux/termux-language-server)](https://github.com/termux/termux-language-server/issues?q=is%3Aissue+is%3Aclosed)
[![github/issues-pr](https://shields.io/github/issues-pr/termux/termux-language-server)](https://github.com/termux/termux-language-server/pulls)
[![github/issues-pr-closed](https://shields.io/github/issues-pr-closed/termux/termux-language-server)](https://github.com/termux/termux-language-server/pulls?q=is%3Apr+is%3Aclosed)
[![github/discussions](https://shields.io/github/discussions/termux/termux-language-server)](https://github.com/termux/termux-language-server/discussions)
[![github/milestones](https://shields.io/github/milestones/all/termux/termux-language-server)](https://github.com/termux/termux-language-server/milestones)
[![github/forks](https://shields.io/github/forks/termux/termux-language-server)](https://github.com/termux/termux-language-server/network/members)
[![github/stars](https://shields.io/github/stars/termux/termux-language-server)](https://github.com/termux/termux-language-server/stargazers)
[![github/watchers](https://shields.io/github/watchers/termux/termux-language-server)](https://github.com/termux/termux-language-server/watchers)
[![github/contributors](https://shields.io/github/contributors/termux/termux-language-server)](https://github.com/termux/termux-language-server/graphs/contributors)
[![github/commit-activity](https://shields.io/github/commit-activity/w/termux/termux-language-server)](https://github.com/termux/termux-language-server/graphs/commit-activity)
[![github/last-commit](https://shields.io/github/last-commit/termux/termux-language-server)](https://github.com/termux/termux-language-server/commits)
[![github/release-date](https://shields.io/github/release-date/termux/termux-language-server)](https://github.com/termux/termux-language-server/releases/latest)

[![github/license](https://shields.io/github/license/termux/termux-language-server)](https://github.com/termux/termux-language-server/blob/main/LICENSE)
[![github/languages](https://shields.io/github/languages/count/termux/termux-language-server)](https://github.com/termux/termux-language-server)
[![github/languages/top](https://shields.io/github/languages/top/termux/termux-language-server)](https://github.com/termux/termux-language-server)
[![github/directory-file-count](https://shields.io/github/directory-file-count/termux/termux-language-server)](https://github.com/termux/termux-language-server)
[![github/code-size](https://shields.io/github/languages/code-size/termux/termux-language-server)](https://github.com/termux/termux-language-server)
[![github/repo-size](https://shields.io/github/repo-size/termux/termux-language-server)](https://github.com/termux/termux-language-server)
[![github/v](https://shields.io/github/v/release/termux/termux-language-server)](https://github.com/termux/termux-language-server)

[![pypi/status](https://shields.io/pypi/status/termux-language-server)](https://pypi.org/project/termux-language-server/#description)
[![pypi/v](https://shields.io/pypi/v/termux-language-server)](https://pypi.org/project/termux-language-server/#history)
[![pypi/downloads](https://shields.io/pypi/dd/termux-language-server)](https://pypi.org/project/termux-language-server/#files)
[![pypi/format](https://shields.io/pypi/format/termux-language-server)](https://pypi.org/project/termux-language-server/#files)
[![pypi/implementation](https://shields.io/pypi/implementation/termux-language-server)](https://pypi.org/project/termux-language-server/#files)
[![pypi/pyversions](https://shields.io/pypi/pyversions/termux-language-server)](https://pypi.org/project/termux-language-server/#files)

Language server for some specific bash scripts:

- Android [Termux](https://termux.dev)
  - [`build.sh`](https://github.com/termux/termux-packages/wiki/Creating-new-package)
  - [`*.subpackage.sh`](https://github.com/termux/termux-packages/wiki/Creating-new-package#subpackage-build-script)
- [ArchLinux](https://archlinux.org)/Windows [Msys2](https://msys2.org)
  - [`PKGBUILD`](https://wiki.archlinux.org/title/PKGBUILD)
  - [`*.install`](https://wiki.archlinux.org/title/PKGBUILD#install)
  - [`makepkg.conf`](https://man.archlinux.org/man/makepkg.conf.5.en)
- [Gentoo](https://www.gentoo.org/)
  - [`*.ebuild`](https://dev.gentoo.org/~zmedico/portage/doc/man/ebuild.5.html)
  - `*.eclass`
  - [`make.conf`](https://dev.gentoo.org/~zmedico/portage/doc/man/make.conf.5.html)
  - [`color.map`](https://dev.gentoo.org/~zmedico/portage/doc/man/color.map.5.html)
- Debian/Ubuntu
  - [`devscripts.conf` and `.devscripts`](https://manpages.ubuntu.com/manpages/bionic/man5/devscripts.conf.5.html)
- zsh
  - [`*.mdd`](https://github.com/zsh-users/zsh/blob/57248b88830ce56adc243a40c7773fb3825cab34/Etc/zsh-development-guide#L285-L288)

A completion for [bash-language-server](https://github.com/bash-lsp/bash-language-server).
Refer [lsp-tree-sitter](https://github.com/neomutt/lsp-tree-sitter).

Extra features:

- complete package names
  - [x] `PKGBUILD`: by [pyalpm](https://github.com/ornitorrincos/pyalpm)
  - [x] `ebuild`: by [portage](https://wiki.gentoo.org/wiki/Portage)
  - [ ] `build.sh`
- linter
  - [x] `PKGBUILD`: by [namcap](https://wiki.archlinux.org/title/Namcap)

## Screenshots

### Diagnostic

![diagnostic](https://github.com/termux/termux-language-server/assets/32936898/598c371f-151d-442f-b782-e504a3d08872)

### Document Link

![document link](https://github.com/neomutt/lsp-tree-sitter/assets/32936898/d3777f3c-9b75-41f9-b6b3-1c4ec55c7283)

### Hover

![package](https://github.com/neomutt/lsp-tree-sitter/assets/32936898/3d9fa906-35ea-4063-a9eb-06282d3e8596)

### Completion

![completion](https://github.com/neomutt/lsp-tree-sitter/assets/32936898/c060690c-071b-41a0-bde5-dce338f4e779)

![arch](https://github.com/termux/termux-language-server/assets/32936898/e10b40c6-515e-4d50-9526-d32ea26b9238)

![license](https://github.com/termux/termux-language-server/assets/32936898/13109df3-30ba-4371-ad0a-aa7f46c8e80a)

![depends](https://github.com/termux/termux-language-server/assets/32936898/a70b41ae-cf4b-44cc-bb10-a54cb5488f30)
