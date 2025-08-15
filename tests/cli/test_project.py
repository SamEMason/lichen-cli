from pathlib import Path
from pytest import MonkeyPatch
from typer.testing import CliRunner

from core.context import Context
from core.utils.io import write_toml
from core.utils.tests import patch_root_with_tmp_path
from cli.main import app

runner = CliRunner()


def test_build_command():
    result = runner.invoke(app, ["project", "build"])
    assert result.exit_code == 0


def test_decimate_command():
    result = runner.invoke(app, ["project", "decimate"])
    assert result.exit_code == 0


def test_destroy_command():
    result = runner.invoke(app, ["project", "destroy", "test_name"])
    assert result.exit_code == 0


def test_new_command(monkeypatch: MonkeyPatch, tmp_path: Path):
    patch_root_with_tmp_path(monkeypatch, tmp_path)

    # Create Context object instance
    ctx = Context()

    # Create scaffold.toml file in tmp_path
    write_toml(ctx.scaffold_file, {"default": [{"nodes": []}]})

    result = runner.invoke(app, ["project", "new", "test_name"])
    assert result.exit_code == 0
