import pytest
from typer.testing import CliRunner

from lichen_cli.main import app

runner = CliRunner()

@pytest.mark.skip()
def test_test_command():
    result = runner.invoke(app, ["test"])
    assert result.exit_code == 0
