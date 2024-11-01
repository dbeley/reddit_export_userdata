with import <nixpkgs> { };

let
  pythonPackages = python3Packages;
in pkgs.mkShell {
  buildInputs = [
    pythonPackages.python

    pythonPackages.praw
    pythonPackages.pyyaml
    pythonPackages.black
  ];

}
