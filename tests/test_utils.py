from pathlib import Path
from lichen.utils.io import make_dir


def test_make_dir(global_cleanup: Path):
    # Create directory test/ with _make_dir()
    make_dir("temp")

    # Determine if the directory exists
    dir_exists = Path("temp").is_dir()
    assert dir_exists == True

