from pathlib import Path
from core.utils.io import (
    get_path,
    get_project_root,
    load_toml,
    make_dir,
    make_file,
    write_toml,
)


def test_get_project_root():
    # File in root
    root_file = "pyproject.toml"

    # Get project root using get_project_root
    project_root = get_project_root()

    assert isinstance(project_root, Path)

    # Determine if pyproject.toml is in the returned root path
    assert (project_root / root_file).exists()


def test_get_path():
    # Prepare path
    filepath = Path("tests/test_utils.py")

    # Get path using get_path
    result = get_path(filepath)

    # Assert returned value is of type Path
    assert isinstance(result, Path)

    # Assert file exists in returned path
    assert result.exists(), f"Expected {result} to exist"


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
    filepath = get_path("tests/test_data/load_toml.toml")
    file_contents = load_toml(filepath=filepath)

    # Assert that the file exists before loading
    assert filepath.exists(), f"Expected {filepath} to exist for test"

    # Assert that the file contents are loaded as expected
    assert file_contents == expected_contents


def test_write_toml(tmp_path: Path):
    # Expected file write key-value pair
    file_content = {"test": "content"}

    # Attempt to write to a test TOML file
    filepath = tmp_path / "write_toml.toml"

    write_toml(filepath=filepath, content=file_content)

    # Assert write_toml.toml exists after file writing
    assert filepath.exists(), f"Expected {filepath} to exist after write_toml()"

    # Load write_toml.toml
    loaded_content = load_toml(filepath=filepath)

    # Assert the loaded content is equivalent to the written content
    assert loaded_content == file_content
