from dataclasses import dataclass

from core.utils.io import get_project_root, load_toml, write_toml

CONFIG_FILENAME = "config.toml"
ALLOWED_KEYS = {"cli_dir", "core_dir", "tmp_dir", "project_name"}


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
        project_root = get_project_root()
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

    def __getitem__(self, key: str):
        return getattr(self, key)

    def __contains__(self, key: str):
        return hasattr(self, key)
