from pathlib import Path
from lichen.config import Config
from lichen.scaffold import scaffold_project
from lichen.utils.io import get_project_root


config = Config()


def test_scaffold_project_creates_project_dir():
    # Test directory
    test_dir = "test_project"

    # Run scaffold_project
    scaffold_project(test_dir)

    # Determine whether root/dev/test_project was created
    assert (get_project_root() / Path(f"dev/{test_dir}")).is_dir()
