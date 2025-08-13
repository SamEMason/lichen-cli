from typer.testing import CliRunner

from cli.main import app

runner = CliRunner()


def test_dev_command():
    result = runner.invoke(app, ["dev"])
    assert result.exit_code == 0
