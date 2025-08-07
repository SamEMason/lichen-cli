from pathlib import Path
from lichen.utils.io import make_dir, make_file


def test_make_dir(global_cleanup: Path):
    # Create directory test/ with _make_dir()
    make_dir("temp")

    # Determine if the directory exists
    dir_exists = Path("temp").is_dir()
    assert dir_exists == True


def test_make_file(global_cleanup: Path):
    # Create temp/ dir for test
    make_dir("temp")

    # Create `test.txt` file
    make_file("temp/test.txt")

    #Determine if the file exists
    file_exists = Path("temp/test.txt").exists()
    assert file_exists == True


