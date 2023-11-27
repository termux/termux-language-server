# Configure

## (Neo)[Vim](https://www.vim.org)

### [coc.nvim](https://github.com/neoclide/coc.nvim)

```json
{
  "languageserver": {
    "termux": {
      "command": "termux-language-server",
      "filetypes": ["sh"]
    },
  }
}
```

### [vim-lsp](https://github.com/prabirshrestha/vim-lsp)

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

## [Neovim](https://neovim.io)

```lua
vim.api.nvim_create_autocmd({ "BufEnter" }, {
  pattern = { "build.sh", "*.subpackage.sh", "PKGBUILD", "*.install",
    "makepkg.conf", "*.ebuild", "*.eclass", "color.map", "make.conf" },
  callback = function()
    vim.lsp.start({
      name = "termux",
      cmd = { "termux-language-server" }
    })
  end,
})
```

## [Emacs](https://www.gnu.org/software/emacs)

```elisp
(make-lsp-client :new-connection
(lsp-stdio-connection
  `(,(executable-find "termux-language-server")))
  :activation-fn (lsp-activate-on "build.sh" "*.subpackage.sh" "PKGBUILD"
"*.install" "makepkg.conf" "*.ebuild" "*.eclass" "color.map" "make.conf")
  :server-id "termux")))
```

## [Sublime](https://www.sublimetext.com)

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
