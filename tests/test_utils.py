from pathlib import Path
from lichen.utils.io import _make_dir, make_root_dir, make_temp_dir  # type: ignore[reportPrivateUsage]


def test_make_dir(global_cleanup: Path):
    # Create directory test/ with _make_dir()
    _make_dir("temp")

    # Determine if the directory exists
    dir_exists = Path("temp").is_dir()
    assert dir_exists == True


def test_temp_dir(global_cleanup: Path):
    # Create directory temp/ with make_temp_dir()
    make_temp_dir()

    # Determine if the directory exists
    dir_exists = Path("temp/").is_dir()
    assert dir_exists == True


def test_root_dir(global_cleanup: Path):
    # Create directory temp/test_project with make_root_dir()
    make_root_dir("test_project")

    # Determine if the directory exists
    dir_exists = Path("test_project/").is_dir()
    assert dir_exists == True
