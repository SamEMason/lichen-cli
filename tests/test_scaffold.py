from lichen_core.config import Config
from lichen_core.scaffold import scaffold_project
from lichen_core.utils.io import get_project_root


config = Config()


def test_scaffold_project_creates_project_dir():
    # Test directory name
    test_dir = "test_project"

    # Run scaffold_project
    scaffold_project(test_dir)

    # Assert_project directory was created
    filepath = get_project_root() / f"dev/{test_dir}"
    assert filepath.is_dir()
