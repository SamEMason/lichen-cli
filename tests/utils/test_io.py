from pathlib import Path
import pytest

from lichen_core.utils.discovery import tool_root
from lichen_core.utils.io import (
    load_toml,
    make_dir,
    make_file,
    write_toml,
)
from tests.utils import path_to_test_data


@pytest.mark.skip()
def test_tool_root():
    # File in root
    root_file = "pyproject.toml"

    # Get project root using tool_root
    project_root = tool_root("lichen")

    assert isinstance(project_root, Path)

    # Determine if pyproject.toml is in the returned root path
    assert (project_root / root_file).exists()


def test_make_dir(tmp_path: Path):
    # Prepare path
    filepath = tmp_path / "temp"

    # Create directory test/ with make_dir()
    make_dir(filepath)

    # Assert temp/ is directory
    assert filepath.is_dir(), f"Expected directory {filepath} to be created"


def test_make_file_makes_file(tmp_path: Path):
    # Prepare path
    filepath = tmp_path / "test.txt"

    # Create directory and file
    make_file(filepath)

    # Assert file exists
    assert filepath.exists(), f"Expected {filepath} to be created"


def test_load_toml():
    # Expected test values
    expected_contents = {"test": {"value": 1}}

    # Load load_toml.toml
    filepath = path_to_test_data("load_toml.toml")
    file_contents = load_toml(filepath=filepath)

    # Assert that the file exists before loading
    assert filepath.exists(), f"Expected {filepath} to exist for test"

    # Assert that the file contents are loaded as expected
    assert file_contents == expected_contents


def test_write_toml(tmp_path: Path):
    # Expected file write key-value pair
    file_content: dict[str, str | None] = {"test": "content"}

    # Attempt to write to a test TOML file
    filepath = tmp_path / "write_toml.toml"

    write_toml(filepath=filepath, content=file_content)

    # Assert write_toml.toml exists after file writing
    assert filepath.exists(), f"Expected {filepath} to exist after write_toml()"

    # Load write_toml.toml
    loaded_content = load_toml(filepath=filepath)

    # Assert the loaded content is equivalent to the written content
    assert loaded_content == file_content
