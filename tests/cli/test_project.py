from pathlib import Path
from pytest import MonkeyPatch, mark
from typer.testing import CliRunner

from lichen_cli.main import app
from tests.utils import (
    copy_file_to_tmp_path,
    get_registry_path,
    use_test_config_data
)

runner = CliRunner()


def test_build_command(monkeypatch: MonkeyPatch, tmp_path: Path):
    use_test_config_data(monkeypatch, tmp_path)
    result = runner.invoke(app, ["project", "build"])
    assert result.exit_code == 0


def test_decimate_command(monkeypatch: MonkeyPatch, tmp_path: Path):
    use_test_config_data(monkeypatch, tmp_path)
    result = runner.invoke(app, ["project", "decimate"])
    assert result.exit_code == 0


def test_destroy_command(monkeypatch: MonkeyPatch, tmp_path: Path):
    use_test_config_data(monkeypatch, tmp_path)
    result = runner.invoke(app, ["project", "destroy", "test_name"])
    assert result.exit_code == 0


@mark.skip()
def test_new_command(monkeypatch: MonkeyPatch, tmp_path: Path):
    # Get test_registry.toml from tests dir
    registry_path = get_registry_path()
    destination = tmp_path / ".scaffold" / "registry.toml"

    copy_file_to_tmp_path(monkeypatch, tmp_path, source=registry_path, dest=destination)
    monkeypatch.chdir(tmp_path)

    assert destination.is_file(), destination.resolve()

    # Invoke the `project new` command
    result = runner.invoke(app, ["project", "new", "test_name"])

    # Assert `project new` command exits cleanly
    assert result.exit_code == 0
