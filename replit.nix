
{ pkgs }: {
  deps = [
    pkgs.portmidi
    pkgs.pkg-config
    pkgs.libpng
    pkgs.libjpeg
    pkgs.freetype
    pkgs.fontconfig
    pkgs.python312
    pkgs.xorg.libX11
    pkgs.xorg.libXext
    pkgs.libGL
    pkgs.SDL2
    pkgs.SDL2_mixer
    pkgs.SDL2_image
    pkgs.SDL2_ttf
    pkgs.cairo
  ];
}
