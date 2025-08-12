import pytest
from pathlib import Path
from pytest import MonkeyPatch
from core.config import Config


def test_config_instantiates_with_defaults():
    expected_values: dict[str, str | None] = {
        "cli_dir": "src/cli",
        "core_dir": "src/core",
        "tmp_dir": "dev",
        "project_name": None,
    }

    # Instantiate config object with default properties
    config = Config()

    # Assertions for expected config properties
    for key, value in expected_values.items():
        assert config.get(key) == value


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
        assert config.get(key) == value


def test_get_method_returns_expected_value():
    expected_values: dict[str, str | None] = {
        "cli_dir": "src/cli",
        "core_dir": "src/core",
        "tmp_dir": "dev",
        "project_name": None,
    }

    # Instantiate config object with default properties
    config = Config()

    # Assertions for expected config properties to match Config.get() return values
    for key, value in expected_values.items():
        assert config.get(key) == value


def test_get_method_with_invalid_key_returns_default():
    expected_value: str = ""

    # Instantiate config object with default properties
    config = Config()

    # Assertions for expected config properties to match Config.get() return values
    assert config.get("NOT_A_KEY", "") == expected_value


def test_save_method_modifies_value_of_key(monkeypatch: MonkeyPatch, tmp_path: Path):
    # Force get_project_root() to return isolated tmp_path
    monkeypatch.setattr("core.config.get_project_root", lambda: tmp_path)

    expected_value = "test_project"

    # Instantiate config object
    config = Config()

    # Save the value: "test_project" to the project_name property
    config.save("project_name", expected_value)

    # Assert config.project_name is equal to saved value
    assert config.project_name == expected_value


def test_save_method_modifies_config_file(monkeypatch: MonkeyPatch, tmp_path: Path):
    # Force get_project_root() to return isolated tmp_path
    monkeypatch.setattr("core.config.get_project_root", lambda: tmp_path)

    expected_value = "test_project"

    # Instantiate config object
    config = Config()

    # Save the value: "test_project" to the project_name property
    config.save("project_name", expected_value)

    path = tmp_path / "config.toml"

    # Assertions for config.toml creation with expected value saved
    assert path.exists()
    assert expected_value in path.read_text()


def test_save_method_raises_keyerror_with_malformed_keys(
    monkeypatch: MonkeyPatch, tmp_path: Path
):
    # Force get_project_root() to return isolated tmp_path
    monkeypatch.setattr("core.config.get_project_root", lambda: tmp_path)

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
    monkeypatch.setattr("core.config.get_project_root", lambda: tmp_path)

    expected_value = "test_project"
    path = tmp_path / "config.toml"

    # Instantiate config object
    config = Config()

    # Assert that config.toml doesn't exist to start
    assert not path.exists()

    # Save the value: "test_project" to the project_name property
    config.save("project_name", expected_value)

    # Assert that config.save() created config.toml
    assert path.exists()
