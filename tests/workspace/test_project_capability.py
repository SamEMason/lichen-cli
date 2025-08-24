from cli.workspace import ProjectCapability, Workspace


def test_project_instantiates_as_type_project_capability():
    # Instantiate Workspace object
    ws = Workspace()

    # Assert Workspace.project is of type ProjectCapability
    assert isinstance(ws.project, ProjectCapability)


def test_project_new_method_is_callable():
    # Instantiate Workspace object
    ws = Workspace()

    # Assert Workspace.project_new method is callable
    assert callable(ws.project.new)
