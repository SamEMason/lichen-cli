import pytest
from pathlib import Path
from pytest import MonkeyPatch
from typing import Any

from core.config import Config, CONFIG_FILENAME, DEFAULT_CONFIGS
from core.context import Context
from core.utils.io import write_toml


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


def test_load_method_loads_data_from_config_file(
    monkeypatch: MonkeyPatch, tmp_path: Path
):
    # Force get_project_root() to return isolated tmp_path
    monkeypatch.setattr("core.context.find_project_root", lambda: tmp_path)

    default_value = None
    loaded_value = "test_project"

    # Create config.toml at root with test property value
    write_toml(tmp_path / CONFIG_FILENAME, {"dev": {"project_name": loaded_value}})

    # Assert default project_name value in memory before load
    context = Context()
    assert context.config["project_name"] == default_value

    # Assert loaded project_name value in memory after load
    context.load()
    assert context.config["project_name"] == loaded_value


def test_load_method_keeps_default_values_when_config_file_is_empty(
    monkeypatch: MonkeyPatch, tmp_path: Path
):
    # Force get_project_root() to return isolated tmp_path
    monkeypatch.setattr("core.context.find_project_root", lambda: tmp_path)

    # Create empty config.toml at root
    write_toml(tmp_path / CONFIG_FILENAME, {})

    # Assert default config properties remain after load
    context = Context()
    context.load()

    for k, v in DEFAULT_CONFIGS.items():
        assert context.config[k] == v


def test_load_method_raises_keyerror_if_loaded_key_not_allowed(
    monkeypatch: MonkeyPatch, tmp_path: Path
):
    # Force get_project_root() to return isolated tmp_path
    monkeypatch.setattr("core.context.find_project_root", lambda: tmp_path)

    bad_property: dict[str, Any | None] = {"dev": {"bad_key": "test_project"}}

    # Create config.toml at root with test property value
    write_toml(tmp_path / CONFIG_FILENAME, bad_property)

    # Assert load method raises KeyError
    with pytest.raises(KeyError):
        Context().load()


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


def test_get_absolute_returns_valid_path():
    # Instantiate Context object
    ctx = Context()

    # Prepare path
    filepath = Path("tests/test_utils.py")

    # Return path from scaffold_dir
    path = ctx.get_absolute(filepath)

    # Assert returned value is of type Path
    assert isinstance(path, Path)


def test_get_absolute_returns_correct_path():
    # Instantiate Context object
    ctx = Context()

    # Prepare path
    filepath = Path("tests/test_utils.py")

    # Return path from scaffold_dir
    path = ctx.get_absolute(filepath)

    # Assert file exists in returned path
    assert path.exists(), f"Expected {path} to exist"
