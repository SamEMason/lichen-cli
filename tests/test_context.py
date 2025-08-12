from core.config import Config
from core.context import Context


def test_context_instantiates_as_context():
    # Instantiate Context object
    ctx = Context()

    # Assert the Context object is of type Context
    assert isinstance(ctx, Context)


def test_context_includes_config_instance():
    # Instantiate Context object
    ctx = Context()

    # Assert the config field is of type Config
    assert isinstance(ctx.config, Config)


def test_config_file_property_returns_valid_path():
    # Instantiate Context object
    ctx = Context()

    # Return path from config_file
    path = ctx.config_file

    # Assert config_file exists
    assert path.exists()


def test_scaffold_dir_property_returns_valid_directory():
    # Instantiate Context object
    ctx = Context()

    # Return path from scaffold_dir
    path = ctx.scaffold_dir

    # Assert scaffold_dir exists
    assert path.is_dir()


def test_scaffold_dir_property_returns_correct_path():
    # Instantiate Context object
    ctx = Context()

    # Return path from scaffold_dir
    path = ctx.scaffold_dir

    # Assert project_root is loaded
    assert ctx.project_root is not None

    # Assert path is correct
    assert path == ctx.project_root / "src" / "core" / "scaffold"


def test_templates_dir_returns_valid_directory():
    # Instantiate Context object
    ctx = Context()

    # Return path from templates_dir
    path = ctx.templates_dir

    # Assert templates_dir exists
    assert path.is_dir()


def test_templates_dir_returns_correct_directory():
    # Instantiate Context object
    ctx = Context()

    # Return path from templates_dir
    path = ctx.templates_dir

    # Assert templates_dir exists
    assert path == ctx.scaffold_dir / "templates"
