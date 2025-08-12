import pytest
from pathlib import Path
from pytest import MonkeyPatch

from core.config import Config, CONFIG_FILENAME, DEFAULT_CONFIGS
from core.utils.io import write_toml


def test_config_instantiates_with_defaults():
    # Instantiate config object with default properties
    config = Config()

    # Assertions for expected config properties
    for key, value in DEFAULT_CONFIGS.items():
        assert config[key] == value


def test_config_instantiates_with_passed_in_values():
    expected_values: dict[str, str] = {
        "cli_dir": "cli",
        "core_dir": "core",
        "tmp_dir": "tmp",
        "project_name": "test_project",
    }

    # Instantiate config object with custom property arguments
    config = Config(
        cli_dir=expected_values["cli_dir"],
        core_dir=expected_values["core_dir"],
        tmp_dir=expected_values["tmp_dir"],
        project_name=expected_values["project_name"],
    )

    # Assertions for expected config properties
    for key, value in expected_values.items():
        assert config[key] == value


def test_load_method_loads_data_from_config_file(
    monkeypatch: MonkeyPatch, tmp_path: Path
):
    # Force get_project_root() to return isolated tmp_path
    monkeypatch.setattr("core.config.find_project_root", lambda: tmp_path)

    default_value = None
    loaded_value = "test_project"

    # Create config.toml at root with test property value
    write_toml(tmp_path / CONFIG_FILENAME, {"project_name": loaded_value})

    # Assert default project_name value in memory before load
    config = Config()
    assert config["project_name"] == default_value

    # Assert loaded project_name value in memory after load
    config.load()
    assert config["project_name"] == loaded_value


def test_load_method_keeps_default_values_when_config_file_is_empty(
    monkeypatch: MonkeyPatch, tmp_path: Path
):
    # Force get_project_root() to return isolated tmp_path
    monkeypatch.setattr("core.config.find_project_root", lambda: tmp_path)

    # Create empty config.toml at root
    write_toml(tmp_path / CONFIG_FILENAME, {})

    # Assert default config properties remain after load
    config = Config()
    config.load()

    for k, v in DEFAULT_CONFIGS.items():
        assert config[k] == v


def test_load_method_raises_keyerror_if_loaded_key_not_allowed(
    monkeypatch: MonkeyPatch, tmp_path: Path
):
    # Force get_project_root() to return isolated tmp_path
    monkeypatch.setattr("core.config.find_project_root", lambda: tmp_path)

    bad_property: dict[str, str | None] = {"bad_key": "test_project"}

    # Create config.toml at root with test property value
    write_toml(tmp_path / CONFIG_FILENAME, bad_property)

    # Assert load method raises KeyError
    with pytest.raises(KeyError):
        Config().load()


def test_save_method_modifies_value_of_key(monkeypatch: MonkeyPatch, tmp_path: Path):
    # Force get_project_root() to return isolated tmp_path
    monkeypatch.setattr("core.config.find_project_root", lambda: tmp_path)

    expected_value = "test_project"

    # Instantiate config object
    config = Config()

    # Save the value: "test_project" to the project_name property
    config.save("project_name", expected_value)

    # Assert config.project_name is equal to saved value
    assert config.project_name == expected_value


def test_save_method_modifies_config_file(monkeypatch: MonkeyPatch, tmp_path: Path):
    # Force get_project_root() to return isolated tmp_path
    monkeypatch.setattr("core.config.find_project_root", lambda: tmp_path)

    expected_value = "test_project"

    # Instantiate config object
    config = Config()

    # Save the value: "test_project" to the project_name property
    config.save("project_name", expected_value)

    path = tmp_path / CONFIG_FILENAME

    # Assertions for config.toml creation with expected value saved
    assert path.exists()
    assert expected_value in path.read_text()


def test_save_method_raises_keyerror_with_malformed_keys(
    monkeypatch: MonkeyPatch, tmp_path: Path
):
    # Force get_project_root() to return isolated tmp_path
    monkeypatch.setattr("core.config.find_project_root", lambda: tmp_path)

    malformed_key = "poject_name"
    value = "test_project"

    # Instantiate config object
    config = Config()

    # Assert config.save() raises KeyError with malformed key
    with pytest.raises(KeyError):
        # Attempt to save the malformed key with the value
        config.save(malformed_key, value)


def test_save_method_creates_config_file_if_none_exist(
    monkeypatch: MonkeyPatch, tmp_path: Path
):
    # Force get_project_root() to return isolated tmp_path
    monkeypatch.setattr("core.config.find_project_root", lambda: tmp_path)

    expected_value = "test_project"
    path = tmp_path / CONFIG_FILENAME

    # Instantiate config object
    config = Config()

    # Assert that config.toml doesn't exist to start
    assert not path.exists()

    # Save the value: "test_project" to the project_name property
    config.save("project_name", expected_value)

    # Assert that config.save() created config.toml
    assert path.exists()


def test_to_dict_method_returns_dict_type():
    # Instantiate config object
    config = Config()

    # Assert to_dict method returns a dict
    assert isinstance(config.to_dict(), dict)


def test_dict_method_returns_in_memory_config_data_as_dict():
    # Expect the default config values to be returned
    expected_values = DEFAULT_CONFIGS

    # Instantiate config object
    config = Config()

    # Call to_dict and store returned dict
    returned_values = config.to_dict()

    # Assert the returned dict contains default config values
    assert returned_values == expected_values
