# Install

## [AUR](https://aur.archlinux.org/packages/termux-language-server)

```sh
yay -S termux-language-server
```

## [NUR](https://nur.nix-community.org/repos/termux)

```nix
{ config, pkgs, ... }:
{
  nixpkgs.config.packageOverrides = pkgs: {
    nur = import
      (
        builtins.fetchTarball
          "https://github.com/nix-community/NUR/archive/master.tar.gz"
      )
      {
        inherit pkgs;
      };
  };
  environment.systemPackages = with pkgs;
      (
        python3.withPackages (
          p: with p; [
            nur.repos.termux.termux-language-server
          ]
        )
      )
}
```

## [Nix](https://nixos.org)

```sh
nix shell github:termux/termux-language-server
```

Run without installation:

```sh
nix run github:termux/termux-language-server -- --help
```

## [PYPI](https://pypi.org/project/termux-language-server)

```sh
pip install termux-language-server
```

See [requirements](requirements) to know `extra_requires`.
