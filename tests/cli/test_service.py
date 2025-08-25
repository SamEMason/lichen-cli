from typer.testing import CliRunner

from lichen_cli.main import app

runner = CliRunner()


def test_add_command():
    result = runner.invoke(app, ["service", "add", "test_name"])
    assert result.exit_code == 0

def test_remove_command():
    result = runner.invoke(app, ["service", "remove", "test_name"])
    assert result.exit_code == 0

