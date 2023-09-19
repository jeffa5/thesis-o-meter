{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  };

  outputs = {
    self,
    nixpkgs,
  }: let
    system = "x86_64-linux";
    pkgs = import nixpkgs {inherit system;};
    python = pkgs.python3.withPackages (ps: [ps.pandas ps.seaborn]);
  in {
    packages.${system}.plot = pkgs.writeShellScriptBin "plot" ''
      ${python}/bin/python ${./plot.py}
    '';

    devShells.${system}.default = pkgs.mkShellNoCC {
      packages = [
        python
      ];
    };
  };
}
