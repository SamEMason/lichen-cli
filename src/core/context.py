from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from core.config import Config, ALLOWED_KEYS, CONFIG_FILENAME
from core.utils.discovery import find_tool_root
from core.utils.io import load_toml, write_toml


ENV_SECTION = "dev"


@dataclass
class Context:
    config: Config = field(default_factory=Config)
    project_root: Optional[Path] = None
    working_root: Path = field(default_factory=Path.cwd)
    selected_set: str = "default"

    def __post_init__(self):
        if self.project_root is None:
            self.project_root = find_tool_root()

    # Config lifecycle methods
    def load_config(self):
        # Get project root directory to write config
        if self.project_root is None:
            raise ValueError("Project root was not initialized.")

        config_location = self.project_root / CONFIG_FILENAME

        if not config_location.exists():
            return

        # Load properties from config.toml
        data = load_toml(config_location)

        section = data.get(ENV_SECTION, {})

        # Iterate through file data and store loaded properties in memory
        for k, v in section.items():
            # If key isn't allowed, raise KeyError
            if k not in ALLOWED_KEYS:
                raise KeyError(f"Unknown key: {k}.")

            # Otherwise store data in memory
            self.config[k] = None if v == "" else v

    def save_config(self, key: str, value: str):
        """Validate and persist config property changes to config.toml."""
        # Validate key is allowed
        if not key in ALLOWED_KEYS:
            raise KeyError(f"Unknown key: {key}.")

        # Get project root directory to write config
        project_root = find_tool_root()
        config_location = project_root / CONFIG_FILENAME

        # If config.toml doesn't exist, create empty dictionary
        if not config_location.exists():
            configs = {}
        else:
            # Else persist config update in config.toml
            configs = load_toml(config_location)

        # Add updated configs to dictionary
        section = configs.setdefault(ENV_SECTION, {})
        section[key] = value
        self.config[key] = value

        # Overwrite config.toml with updated configs
        write_toml(config_location, content=configs)
