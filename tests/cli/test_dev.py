from typer.testing import CliRunner

from lichen_cli.main import app

runner = CliRunner()


def test_dev_command():
    result = runner.invoke(app, ["dev"])
    assert result.exit_code == 0
