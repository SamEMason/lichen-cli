from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from core.config import Config, ALLOWED_KEYS, CONFIG_FILENAME
from core.utils.discovery import find_project_root
from core.utils.io import load_toml


@dataclass
class Context:
    config: Config = field(default_factory=Config)
    project_root: Optional[Path] = None

    def __post_init__(self):
        if self.project_root is None:
            self.project_root = find_project_root()

    # Internal guard
    def _root(self) -> Path:
        assert self.project_root is not None
        return self.project_root

    # Config lifecycle methods
    def load(self):
        # Get project root directory to write config
        project_root = find_project_root()
        config_location = project_root / CONFIG_FILENAME

        if not config_location.exists():
            return

        # Load properties from config.toml
        data = load_toml(config_location)

        section = data.get("dev", {})

        # Iterate through file data and store loaded properties in memory
        for k, v in section.items():
            # If key isn't allowed, raise KeyError
            if k not in ALLOWED_KEYS:
                raise KeyError(f"Unknown key: {k}.")

            # Otherwise store data in memory
            self.config[k] = None if v == "" else v

    # Canonical paths (callers should use these)
    @property
    def config_file(self) -> Path:
        return self._root() / CONFIG_FILENAME

    @property
    def scaffold_dir(self):
        return self._root() / "src" / "core" / "scaffold"

    @property
    def templates_dir(self):
        return self.scaffold_dir / "templates"

    def get_absolute(self, filepath: str | Path) -> Path:
        """Return absolute path under the project root."""
        path = Path(filepath).expanduser()
        if path.is_absolute():
            return path.resolve()
        return (self._root() / filepath).resolve()
