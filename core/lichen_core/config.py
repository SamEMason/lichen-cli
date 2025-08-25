from dataclasses import dataclass
from typing import Any


CONFIG_FILENAME: str = "config.toml"
ALLOWED_KEYS: tuple[str, ...] = ("tmp_dir", "project_name")
DEFAULT_CONFIGS: dict[str, str | None] = {
    "tmp_dir": "dev",
    "project_name": None,
}


@dataclass
class Config:
    tmp_dir: str = "dev"
    project_name: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {k: self[k] for k in ALLOWED_KEYS}

    def __getitem__(self, key: str):
        return getattr(self, key)

    def __setitem__(self, key: str, value: Any):
        return setattr(self, key, value)

    def __contains__(self, key: str):
        return hasattr(self, key)
