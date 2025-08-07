import pytest
from pathlib import Path
from lichen.utils.io import get_path, get_project_root, load_toml, make_dir, make_file


def test_get_project_root():
    # File in root
    root_file = "pyproject.toml"

    # Get project root using get_project_root
    project_root = get_project_root()

    # Determine if pyproject.toml is in the returned root path
    assert (project_root / root_file).exists()


def test_get_path():
    # File to test against
    target_file = "tests/test_utils.py"

    # Determine if this file exists in the returned path
    assert get_path(target_file).exists()


def test_make_dir(global_cleanup: Path):
    # Create directory test/ with _make_dir()
    make_dir("temp")

    # Determine if the directory exists
    dir_exists = Path("temp").is_dir()
    assert dir_exists == True


def test_make_file_makes_file(global_cleanup: Path):
    # Create temp/ dir for test
    make_dir("temp")

    # Create `test.txt` file
    make_file("temp/test.txt")

    # Determine if the file exists
    file_exists = Path("temp/test.txt").exists()
    assert file_exists == True


def test_make_file_raises_on_read_mode():
    test_file = "test_file.txt"
    mode = "r"

    with pytest.raises(ValueError, match="Cannot use read mode to make a file"):
        make_file(test_file, mode)


def test_load_toml():
    # Expected test values
    expected_contents = {"test": {"value": 1}}

    # Read file: `load_toml.toml`
    filepath = get_path("tests/test_data/load_toml.toml")
    file_contents = load_toml(filepath=str(filepath))

    # Assert that the file contents are loaded as expected
    assert file_contents == expected_contents
