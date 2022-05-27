"""Symlink tech to klayout."""
import os
import pathlib
import sys

if sys.platform == "win32":
    klayout_folder = "KLayout"
else:
    klayout_folder = ".klayout"


cwd = pathlib.Path(__file__).resolve().parent
home = pathlib.Path.home()
src = cwd / "openfasoc" / "klayout" / "sky130"
dest_folder = home / klayout_folder / "tech"
dest_folder.mkdir(exist_ok=True, parents=True)
dest = dest_folder / "sky130"


def install_tech(src, dest):
    """Installs tech."""
    if dest.exists():
        print(f"tech already installed in {dest}")
        return

    try:
        os.symlink(src, dest)
    except Exception:
        os.remove(dest)
        os.symlink(src, dest)
    print(f"layermap installed to {dest}")


if __name__ == "__main__":
    install_tech(src=src, dest=dest)
