from pathlib import Path
from pytest import MonkeyPatch
from shutil import copyfile
from typing import Any, Optional

from lichen_core.config import CONFIG_FILENAME
from lichen_core.registry import ScaffoldSet
from lichen_core.scaffold import Node
from lichen_cli.utils import find_tool_root
from lichen_core.utils.io import write_toml


def get_test_data(filename: str):
    """Retrieve absolute filepath for test data files"""
    root = find_tool_root(lichen_root=True)
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
    monkeypatch: MonkeyPatch, tmp_path: Path, module: Optional[str] = "utils"
):
    """Patches find_tool_root() with tmp_path fixture"""
    # Force find_tool_root to return isolated tmp_path
    monkeypatch.setattr(f"lichen_cli.{module}.find_tool_root", lambda: tmp_path)


###### NOTE: EXTEND TO HANDLE FILE NAME CHANGES AND DIRECTORY NESTING
def copy_file_to_tmp_path(
    monkeypatch: MonkeyPatch, tmp_path: Path, source: Path, dest: Path
):
    patch_root_with_tmp_path(monkeypatch, tmp_path)

    dest.parent.mkdir(parents=True, exist_ok=True)

    # Copy file from source path to tmp_path
    copyfile(source, dest)


def use_test_config_data(
    monkeypatch: MonkeyPatch, tmp_path: Path, module: Optional[str] = "utils"
):
    patch_root_with_tmp_path(monkeypatch, tmp_path, module)

    test_config_path = path_to_test_data("test_config.toml")
    dest = tmp_path / CONFIG_FILENAME

    dest.parent.mkdir(parents=True, exist_ok=True)
    copyfile(test_config_path, dest)


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
    # Instatiate registry file path with default value if None
    if path is None:
        path = path_to_test_data("test_registry.toml")
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
    nodes: list[Node] = [
        Node(type="file", path=Path("testpath"), template=Path("testtemp"))
    ],
) -> ScaffoldSet:

    return ScaffoldSet(
        set_name=set_name,
        version=version,
        description=description,
        nodes=nodes,
    )


def path_to_test_data(*parts: str) -> Path:
    return Path(__file__).parent / ".test_data" / Path(*parts)


def get_registry_path():
    return path_to_test_data("test_registry.toml")
