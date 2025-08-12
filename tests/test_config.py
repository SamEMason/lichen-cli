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


def test_config_get_returns_expected_value():
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


def test_config_get_with_invalid_key_returns_default():
    expected_value: str = ""

    # Instantiate config object with default properties
    config = Config()

    # Assertions for expected config properties to match Config.get() return values
    assert config.get("NOT_A_KEY", "") == expected_value
