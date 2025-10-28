# Configure

- For windows, change `~/.config` to `~/AppData/Local`
- For macOS, change `~/.config` to `~/Library`

## [Neovim](https://neovim.io) / [Vim](https://www.vim.org)

### [coc.nvim](https://github.com/neoclide/coc.nvim)

`~/.config/nvim/coc-settings.json`:

```json
{
  "languageserver": {
    "termux": {
      "command": "termux-language-server",
      "filetypes": [
        "sh"
      ]
    }
  }
}
```

### [vim-lsp](https://github.com/prabirshrestha/vim-lsp)

Neovim - `~/.config/nvim/init.vim`:\
Vim - `~/.config/vim/vimrc`:

```vim
if executable('termux-language-server')
  augroup lsp
    autocmd!
    autocmd User lsp_setup call lsp#register_server({
          \ 'name': 'termux',
          \ 'cmd': {server_info->['termux-language-server']},
          \ 'whitelist': ['sh'],
          \ })
  augroup END
endif
```

### [nvim-lspconfig](https://github.com/neovim/nvim-lspconfig) (upstream configs)

Example via [`lazy.nvim`](https://github.com/folke/lazy.nvim)\
For other options see: [nvim-lspconfig#install](https://github.com/neovim/nvim-lspconfig#install)\
Or the documentation for your plugin manager of choice.

`~/.config/nvim/init.vim`:

```lua
require('lazy').setup({
  -- [...]
  { 'neovim/nvim-lspconfig' },
  -- [...]
})

vim.lsp.enable('termux_language_server')
```

## [Emacs](https://www.gnu.org/software/emacs)

`~/.config/emacs/init.el`:

```elisp
(make-lsp-client :new-connection
(lsp-stdio-connection
  `(,(executable-find "termux-language-server")))
  :activation-fn (lsp-activate-on "build.sh" "*.subpackage.sh" "PKGBUILD"
"*.install" "makepkg.conf" "*.ebuild" "*.eclass" "color.map" "make.conf")
  :server-id "termux")))
```

## [Helix](https://helix-editor.com/)

`~/.config/helix/languages.toml`:

```toml
[[language]]
name = "sh"
language-servers = ["termux-language-server"]

[language_server.termux-language-server]
command = "termux-language-server"
```

## [KaKoune](https://kakoune.org/)

### [kak-lsp](https://github.com/kak-lsp/kak-lsp)

`~/.config/kak-lsp/kak-lsp.toml`:

```toml
[language_server.termux-language-server]
filetypes = ["sh"]
command = "termux-language-server"
```

## [Sublime](https://www.sublimetext.com)

`~/.config/sublime-text-3/Packages/Preferences.sublime-settings`:

```json
{
  "clients": {
    "termux": {
      "command": [
        "termux-language-server"
      ],
      "enabled": true,
      "selector": "source.sh"
    }
  }
}
```

## [Visual Studio Code](https://code.visualstudio.com/)

[Official support for generic LSP clients is pending](https://github.com/microsoft/vscode/issues/137885).

### [vscode-glspc](https://gitlab.com/ruilvo/vscode-glspc)

`~/.config/Code/User/settings.json`:

```json
{
  "glspc.serverPath": "termux-language-server",
  "glspc.languageId": "bash"
}
```
