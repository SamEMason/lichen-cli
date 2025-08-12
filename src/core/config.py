from dataclasses import dataclass
from typing import Any

from core.utils.discovery import find_project_root
from core.utils.io import load_toml, write_toml


CONFIG_FILENAME: str = "config.toml"
ALLOWED_KEYS: tuple[str, ...] = ("cli_dir", "core_dir", "tmp_dir", "project_name")
DEFAULT_CONFIGS: dict[str, str | None] = {
    "cli_dir": "src/cli",
    "core_dir": "src/core",
    "tmp_dir": "dev",
    "project_name": None,
}


@dataclass
class Config:
    cli_dir: str = "src/cli"
    core_dir: str = "src/core"
    tmp_dir: str = "dev"
    project_name: str | None = None

    def save(self, key: str, value: str):
        """Validate and persist config property changes to config.toml."""
        # Validate key is allowed
        if not key in ALLOWED_KEYS:
            raise KeyError(f"Unknown key: {key}.")

        # Set config key with inputted value
        setattr(self, key, value)

        # Get project root directory to write config
        project_root = find_project_root()
        config_location = project_root / CONFIG_FILENAME

        # If config.toml doesn't exist, create empty dictionary
        if not config_location.exists():
            configs = {}
        else:
            # Else persist config update in config.toml
            configs = load_toml(config_location)

        # Add updated configs to dictionary
        section = configs.setdefault(self.tmp_dir, {})
        section[key] = value

        # Overwrite config.toml with updated configs
        write_toml(config_location, content=configs)

    def to_dict(self) -> dict[str, Any]:
        return {k: self[k] for k in ALLOWED_KEYS}

    def __getitem__(self, key: str):
        return getattr(self, key)

    def __setitem__(self, key: str, value: Any):
        return setattr(self, key, value)

    def __contains__(self, key: str):
        return hasattr(self, key)
