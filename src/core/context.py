from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from core.config import Config, CONFIG_FILENAME
from core.utils.discovery import find_project_root


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
