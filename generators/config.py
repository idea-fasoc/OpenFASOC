""" store configuration
"""

__all__ = ["PATH"]

import pathlib

home = pathlib.Path.home()
cwd = pathlib.Path.cwd()
cwd_config = cwd / "config.yml"

home_config = home / ".config" / "OpenFASoC.yml"
config_dir = home / ".config"
config_dir.mkdir(exist_ok=True)
module_path = pathlib.Path(__file__).parent.absolute()
repo_path = module_path.parent


class Path:
    module = module_path
    repo = repo_path


PATH = Path()

if __name__ == "__main__":
    print(PATH)
