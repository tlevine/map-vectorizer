with import <nixpkgs> {}; {
  mapVectorizer = stdenv.mkDerivation {
    name = "mapVectorizer";
    buildInputs = [
      gimp python35Packages.pillow
    ];
    PYTHONPATH = "${python35Packages.pillow}/a";
  };  
}
