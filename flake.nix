{
  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";
  inputs.python-setuptools-generate.url = "github:Freed-Wu/setuptools-generate";
  outputs = { self, nixpkgs, flake-utils, python-setuptools-generate }:
    flake-utils.lib.eachDefaultSystem
      (system:
        let setuptools-generate = python-setuptools-generate.packages.${system}.default; in
        with nixpkgs.legacyPackages.${system};
        with python3.pkgs;
        {
          formatter = nixpkgs-fmt;
          packages.default = buildPythonApplication rec {
            name = "termux-language-server";
            src = self;
            format = "pyproject";
            disabled = pythonOlder "3.6";
            propagatedBuildInputs = [
            ];
            nativeCheckInputs = [
              setuptools-generate
            ];
            pythonImportsCheck = [
              "termux_language_server"
            ];
          };
        }
      );
}
