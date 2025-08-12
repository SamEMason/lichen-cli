from core.config import Config, DEFAULT_CONFIGS


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
