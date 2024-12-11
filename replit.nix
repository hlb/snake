
{ pkgs }: {
  deps = [
    pkgs.python312
    pkgs.xorg.libX11
    pkgs.xorg.libXext
    pkgs.libGL
    pkgs.SDL2
    pkgs.SDL2_mixer
    pkgs.SDL2_image
    pkgs.SDL2_ttf
  ];
}
