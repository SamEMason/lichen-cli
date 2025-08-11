from core.utils.io import get_project_root, load_toml, write_toml


class Config:
    def __init__(
        self,
        cli_dir: str = "src/cli",
        core_dir: str = "src/core",
        mode: str = "dev",
        temp_dir: str = "dev",
    ):
        self.mode = mode
        self.cli_dir = cli_dir
        self.core_dir: str = core_dir

        self.project_name: str | None = None
        self.temp_dir = temp_dir

    def get_cli_dir(self, filepath: str):
        return f"{self.cli_dir}/{filepath}"

    def save(self, config_key: str, value: str):
        # Set config key with inputted value
        setattr(self, config_key, value)

        # Get project root directory to write config
        project_root = get_project_root()
        config_location = project_root / "config.toml"

        # Persist config update in config.toml
        configs = load_toml(config_location)
        print(configs)

        # Add updated configs to dictionary
        section = configs.setdefault(self.mode, {})
        print(section)

        section[config_key] = value
        print(section)

        # Overwrite config.toml with updated configs
        write_toml(config_location, content=configs)
