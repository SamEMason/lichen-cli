from pathlib import Path
from pytest import MonkeyPatch
from typer.testing import CliRunner

from core.context import Context
from core.utils.io import write_toml
from core.utils.tests import patch_root_with_tmp_path
from cli.main import app

runner = CliRunner()


def test_build_command(monkeypatch: MonkeyPatch, tmp_path: Path):
    patch_root_with_tmp_path(monkeypatch, tmp_path)
    result = runner.invoke(app, ["project", "build"])
    assert result.exit_code == 0


def test_decimate_command(monkeypatch: MonkeyPatch, tmp_path: Path):
    patch_root_with_tmp_path(monkeypatch, tmp_path)
    result = runner.invoke(app, ["project", "decimate"])
    assert result.exit_code == 0


def test_destroy_command(monkeypatch: MonkeyPatch, tmp_path: Path):
    patch_root_with_tmp_path(monkeypatch, tmp_path)
    result = runner.invoke(app, ["project", "destroy", "test_name"])
    assert result.exit_code == 0


def test_new_command(monkeypatch: MonkeyPatch, tmp_path: Path):
    patch_root_with_tmp_path(monkeypatch, tmp_path)

    # Instantiate Context object
    ctx = Context()

    # Create temporary scaffold.toml file within tmp_path
    if ctx.project_root is None:
        raise ValueError("Registry file path was not initialized.")

    registry_path = ctx.project_root / "src/core/scaffold/scaffold.toml"

    write_toml(
        registry_path,
        {
            "default": {
                "version": "0.0.1",
                "description": "A test description.",
                "nodes": [],
            }
        },
    )

    # Invoke the `project new` command
    result = runner.invoke(app, ["project", "new", "test_name"])

    # Assert `project new` command exits cleanly
    assert result.exit_code == 0
