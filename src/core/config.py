from dataclasses import dataclass
from pathlib import Path
from typing import Any

from core.utils.io import get_project_root, load_toml, write_toml

CONFIG_FILENAME = "config.toml"
ALLOWED_KEYS = {"cli_dir", "core_dir", "tmp_dir", "project_name"}


@dataclass
class Config:
    cli_dir: str = "src/cli"
    core_dir: str = "src/core"
    tmp_dir: str = "dev"
    project_name: str | None = None

    def get(self, key: str, default: str = ""):
        return getattr(self, key, default)

    def save(self, config_key: str, value: str):
        # Set config key with inputted value
        setattr(self, config_key, value)

        # Get project root directory to write config
        project_root = get_project_root()
        config_location = project_root / "config.toml"

        # Persist config update in config.toml
        configs = load_toml(config_location)
        print(configs)

        # Add updated configs to dictionary
        section = configs.setdefault(self.tmp_dir, {})
        print(section)

        section[config_key] = value
        print(section)

        # Overwrite config.toml with updated configs
        write_toml(config_location, content=configs)
