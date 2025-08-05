import os
from pathlib import Path
from lichen import utils


def test_make_dir(global_cleanup: Path):
    # Create directory test/ with _make_dir()
    utils._make_dir("temp")  # type: ignore[reportPrivateUsage]

    # Determine if the directory exists
    dir_exists = os.path.isdir("temp")
    assert dir_exists == True


def test_temp_dir(global_cleanup: Path):
    # Create directory temp/ with make_temp_dir()
    utils.make_temp_dir()

    # Determine if the directory exists
    dir_exists = os.path.isdir("temp/")
    assert dir_exists == True


def test_root_dir(global_cleanup: Path):
    # Create directory temp/test_project with make_root_dir()
    utils.make_root_dir("test_project")

    # Determine if the directory exists
    dir_exists = os.path.isdir("test_project/")
    assert dir_exists == True
