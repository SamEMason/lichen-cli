from typer.testing import CliRunner

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


def test_new_command():
    result = runner.invoke(app, ["project", "new", "test_name"])
    assert result.exit_code == 0
