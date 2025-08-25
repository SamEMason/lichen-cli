import pytest
from pathlib import Path
from pytest import MonkeyPatch
from typing import Any

from lichen_core.config import Config, CONFIG_FILENAME, DEFAULT_CONFIGS
from lichen_core.context import Context
from lichen_core.utils.io import write_toml
from tests.utils import patch_root_with_tmp_path


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


@pytest.mark.skip()
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


@pytest.mark.skip()
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


@pytest.mark.skip()
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


@pytest.mark.skip()
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


@pytest.mark.skip()
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
