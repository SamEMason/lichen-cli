from pathlib import Path
from pytest import MonkeyPatch

from core.context import Context
from core.workspace import Workspace
from core.utils.tests import make_test_config


def test_workspace_instantiates_as_workspace():
    # Instantiate workspace object
    ws = Workspace()

    # Assert workspace object is of type Workspace
    assert isinstance(ws, Workspace)


def test_workspace_context_property_instantiates_as_context():
    # Instantiate workspace object
    ws = Workspace()

    # Assert workspace.context property is of type Context
    assert isinstance(ws.context, Context)


def test_workspace_context_instantiates_as_passed_in_context(
    monkeypatch: MonkeyPatch, tmp_path: Path
):
    # Force get_project_root() to return isolated tmp_path
    monkeypatch.setattr("core.context.find_project_root", lambda: tmp_path)

    modified_key = "project_name"
    modified_value = "test_project"

    # Instantiate workspace object
    ctx = Context()
    ctx.config[modified_key] = modified_value

    # Instantiate workspace object
    ws = Workspace(ctx)

    # Assert workspace.context is the exact instance passed in
    assert ws.context == ctx

    # Assert workspace.context property is of type Context
    assert ws.context.config[modified_key] == modified_value


def test_workspace_context_instantiates_default_without_passed_in_context(
    monkeypatch: MonkeyPatch, tmp_path: Path
):
    # Force get_project_root() to return isolated tmp_path
    monkeypatch.setattr("core.context.find_project_root", lambda: tmp_path)

    expected_key = "project_name"
    expected_value = None

    # Instantiate workspace object
    ctx = Context()
    ctx.config[expected_key] = expected_value

    # Instantiate workspace object
    ws = Workspace()

    # Assert workspace.context is not the out of scope context
    assert ws.context is not ctx

    # Assert workspace.context property is of type Context
    assert ws.context.config[expected_key] == expected_value


def test_workspace_auto_load_true_reads_disk(monkeypatch: MonkeyPatch, tmp_path: Path):
    # Create config.toml in tmp_path with test_data
    test_data = {"dev": {"project_name": "test_project"}}
    make_test_config(monkeypatch, tmp_path, test_data)

    # Instantiate workspace object with autoload set to True
    ws = Workspace(autoload=True)

    # Assert that the data written to config.toml is loaded into ws.context.config
    assert ws.context.config["project_name"] == "test_project"


def test_workspace_auto_load_false_does_not_read_disk(
    monkeypatch: MonkeyPatch, tmp_path: Path
):
    # Create config.toml in tmp_path with test_data
    test_data = {"dev": {"project_name": "test_project"}}
    make_test_config(monkeypatch, tmp_path, test_data)

    # Instantiate workspace object with autoload set to False
    ws = Workspace(autoload=False)

    # Assert that the data written to config.toml is NOT loaded into ws.context.config
    assert ws.context.config["project_name"] == None
