import subprocess
from pathlib import Path
from pytest import MonkeyPatch
from shutil import copyfile
from typing import Any, Optional

from core.config import CONFIG_FILENAME
from core.context import Context
from core.registry import ScaffoldSet
from core.scaffold import Node
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


def registry_arguments(
    path: Optional[str | Path] = None, selected_set: Optional[str] = None
) -> tuple[Path, str]:

    ctx = Context()

    # Instatiate registry file path with default value if None
    if path is None:
        path = ctx.test_dir / ".test_data" / "test_registry.toml"
    else:
        path = Path(path)

    # Instatiate selected_set with default value if None
    if selected_set is None:
        selected_set = "test_set"

    return path, selected_set


def expected_scaffold_set_values(
    set_name: str = "test_set",
    version: str = "0.0.1",
    description: str = "Test scaffold.",
    nodes: list[Node] = [Node(type="file", path="testpath", template="testtemp")],
) -> ScaffoldSet:

    return ScaffoldSet(
        set_name=set_name,
        version=version,
        description=description,
        nodes=nodes,
    )


###### NOTE: EXTEND TO HANDLE FILE NAME CHANGES AND DIRECTORY NESTING
def copy_file_to_tmp_path(monkeypatch: MonkeyPatch, tmp_path: Path, source: Path):
    patch_root_with_tmp_path(monkeypatch, tmp_path)

    # Copy file from source path to tmp_path
    copyfile(source, tmp_path)
