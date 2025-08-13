import pytest
from pathlib import Path
from pytest import MonkeyPatch
from typing import Any

from core.config import Config, CONFIG_FILENAME, DEFAULT_CONFIGS
from core.context import Context
from core.utils.io import make_dir, write_toml
from core.utils.tests import patch_root_with_tmp_path


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


def test_load_config_method_loads_data_from_config_file(
    monkeypatch: MonkeyPatch, tmp_path: Path
):
    patch_root_with_tmp_path(monkeypatch, tmp_path)

    default_value = None
    loaded_value = "test_project"

    # Create config.toml at root with test property value
    write_toml(tmp_path / CONFIG_FILENAME, {"dev": {"project_name": loaded_value}})

    # Assert default project_name value in memory before load
    context = Context()
    assert context.config["project_name"] == default_value

    # Assert loaded project_name value in memory after load
    context.load_config()
    assert context.config["project_name"] == loaded_value


def test_load_config_method_keeps_default_values_when_config_file_is_empty(
    monkeypatch: MonkeyPatch, tmp_path: Path
):
    patch_root_with_tmp_path(monkeypatch, tmp_path)

    # Create empty config.toml at root
    write_toml(tmp_path / CONFIG_FILENAME, {})

    # Assert default config properties remain after load
    context = Context()
    context.load_config()

    for k, v in DEFAULT_CONFIGS.items():
        assert context.config[k] == v


def test_load_config_method_raises_keyerror_if_loaded_key_not_allowed(
    monkeypatch: MonkeyPatch, tmp_path: Path
):
    patch_root_with_tmp_path(monkeypatch, tmp_path)

    bad_property: dict[str, Any | None] = {"dev": {"bad_key": "test_project"}}

    # Create config.toml at root with test property value
    write_toml(tmp_path / CONFIG_FILENAME, bad_property)

    # Assert load method raises KeyError
    with pytest.raises(KeyError):
        Context().load_config()


def test_save_method_modifies_value_of_key(monkeypatch: MonkeyPatch, tmp_path: Path):
    patch_root_with_tmp_path(monkeypatch, tmp_path)

    expected_value = "test_project"

    # Instantiate context object
    context = Context()

    # Save the value: "test_project" to the project_name property
    context.save_config("project_name", expected_value)

    # Assert config.project_name is equal to saved value
    assert context.config.project_name == expected_value


def test_save_method_modifies_config_file(monkeypatch: MonkeyPatch, tmp_path: Path):
    patch_root_with_tmp_path(monkeypatch, tmp_path)

    expected_value = "test_project"

    # Instantiate context object
    context = Context()

    # Save the value: "test_project" to the project_name property
    context.save_config("project_name", expected_value)

    path = tmp_path / CONFIG_FILENAME

    # Assertions for config.toml creation with expected value saved
    assert path.exists()
    assert expected_value in path.read_text()


def test_save_method_raises_keyerror_with_malformed_keys(
    monkeypatch: MonkeyPatch, tmp_path: Path
):
    patch_root_with_tmp_path(monkeypatch, tmp_path)

    malformed_key = "poject_name"
    value = "test_project"

    # Instantiate context object
    context = Context()

    # Assert config.save_config() raises KeyError with malformed key
    with pytest.raises(KeyError):
        # Attempt to save the malformed key with the value
        context.save_config(malformed_key, value)


def test_save_method_creates_config_file_if_none_exist(
    monkeypatch: MonkeyPatch, tmp_path: Path
):
    patch_root_with_tmp_path(monkeypatch, tmp_path)

    expected_value = "test_project"
    path = tmp_path / CONFIG_FILENAME

    # Instantiate context object
    context = Context()

    # Assert that config.toml doesn't exist to start
    assert not path.exists()

    # Save the value: "test_project" to the project_name property
    context.save_config("project_name", expected_value)

    # Assert that config.save_config() created config.toml
    assert path.exists()


def test_config_file_returns_valid_path():
    # Instantiate Context object
    ctx = Context()

    # Return path from config_file
    path = ctx.config_file

    # Assert config_file exists
    assert path.exists()


def test_scaffold_dir_returns_valid_directory():
    # Instantiate Context object
    ctx = Context()

    # Return path from scaffold_dir
    path = ctx.scaffold_dir

    # Assert scaffold_dir exists
    assert path.is_dir()


def test_scaffold_dir_returns_correct_path():
    # Instantiate Context object
    ctx = Context()

    # Return path from scaffold_dir
    path = ctx.scaffold_dir

    # Assert project_root is loaded
    assert ctx.project_root is not None

    # Assert path is correct
    assert path == ctx.project_root / "src" / "core" / "scaffold"


def test_scaffold_file_returns_valid_path():
    # Instantiate Context object
    ctx = Context()

    # Return path from scaffold_file
    path = ctx.scaffold_file

    # Assert project_root is loaded
    assert path.exists()


def test_scaffold_file_returns_correct_path():
    # Instantiate Context object
    ctx = Context()

    # Return path from scaffold_dir
    path = ctx.scaffold_file

    # Assert project_root is loaded
    assert ctx.project_root is not None

    # Assert path is correct
    assert path == ctx.scaffold_dir / "scaffold.toml"


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


def test_temporary_directory_returns_valid_path():
    # Instantiate Context object
    ctx = Context()

    # Return path from scaffold_dir
    path = ctx.temporary_dir

    # Assert returned value is of type Path
    assert isinstance(path, Path | None)


def test_temporary_directory_returns_correct_path_if_exists(
    monkeypatch: MonkeyPatch, tmp_path: Path
):
    patch_root_with_tmp_path(monkeypatch, tmp_path)

    # Instantiate Context object
    ctx = Context()

    # Create temporary directory
    make_dir(tmp_path / ctx.config.tmp_dir)

    # Return path from scaffold_dir
    path = ctx.temporary_dir

    # Assert returned path is not None
    assert path is not None

    # Assert file exists in returned path
    assert path.exists(), f"Expected {path} to exist"


def test_temporary_directory_returns_None_if_it_does_not_exist(
    monkeypatch: MonkeyPatch, tmp_path: Path
):
    patch_root_with_tmp_path(monkeypatch, tmp_path)

    # Instantiate Context object
    ctx = Context()

    # Return path from scaffold_dir
    path = ctx.temporary_dir

    # Assert returned path is None
    assert path == None


def test_path_from_cwd_returns_valid_path(monkeypatch: MonkeyPatch, tmp_path: Path):
    patch_root_with_tmp_path(monkeypatch, tmp_path)

    # Instantiate Context object
    ctx = Context()

    parent_test_path = Path("parent")
    child_test_path = parent_test_path / "child"
    (tmp_path / parent_test_path / child_test_path).mkdir(parents=True)

    monkeypatch.chdir(tmp_path / parent_test_path)

    assert ctx.cwd == tmp_path / parent_test_path

    # Return path from path_from_cwd
    path = ctx.path_from_cmd(child_test_path)

    # Assert returned path is None
    assert path == Path(tmp_path / parent_test_path / child_test_path)
