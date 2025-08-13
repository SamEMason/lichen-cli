import subprocess
from pathlib import Path
from pytest import MonkeyPatch
from typing import Any

from core.config import CONFIG_FILENAME
from core.utils.discovery import find_project_root
from core.utils.io import write_toml


def run_tests():
    """Run tests using `pytest`"""
    subprocess.run(["pytest"])


def get_test_data(filename: str):
    """Retrieve absolute filepath for test data files"""
    root = find_project_root()
    relative_path = "tests/.test_data"
    target = root / relative_path / filename

    # Raise FileNotFoundError if file doesn't exist at this path
    if not target.exists():
        raise FileNotFoundError(f"File {filename} does not exist at {target}.")

    # Raise IsADirectoryError if the filename argument is a directory path
    if target.is_dir():
        raise IsADirectoryError(
            f"Filepath argument {filename} is a directory path not a filepath"
        )

    # Otherwise return the target path
    return target


def patch_root_with_tmp_path(
    monkeypatch: MonkeyPatch, tmp_path: Path, module: str = "context"
):
    """Patches find_project_root() with tmp_path fixture"""
    # Force get_project_root() to return isolated tmp_path
    monkeypatch.setattr(f"core.{module}.find_project_root", lambda: tmp_path)


def make_test_config(
    monkeypatch: MonkeyPatch, tmp_path: Path, data: dict[str, Any] | None = None
):
    patch_root_with_tmp_path(monkeypatch, tmp_path)

    # Build path from tmp_path to config.toml
    path = tmp_path / CONFIG_FILENAME

    # Create config.toml file
    write_toml(path, data)
