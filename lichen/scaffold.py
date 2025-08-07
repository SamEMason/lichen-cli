from .config import Config
from lichen.utils.io import make_root_dir, make_temp_dir


def create_monorepo(name: str):
    config = Config()

    # Nest directory structure in temp/ in dev mode
    if config.mode == "dev":
        # Create temp/ directory
        make_temp_dir()

        # Append `name` with temp/
        name = f"{config.temp_dir}/{name}"

    # Create root project directory
    make_root_dir(name)

