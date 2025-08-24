from cli.workspace.client import ClientCapability
from cli.workspace import Workspace


def test_project_instantiates_as_type_client_capability():
    # Instantiate Workspace object
    ws = Workspace()

    # Assert Workspace.client is of type clientCapability
    assert isinstance(ws.client, ClientCapability)


def test_client_build_method_is_callable():
    # Instantiate Workspace object
    ws = Workspace()

    # Assert Workspace.project_new method is callable
    assert callable(ws.client.build)
