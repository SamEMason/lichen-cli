from pathlib import Path
from pytest import MonkeyPatch

from core.context import Context
from core.scaffold import Node, Scaffolder
from core.utils.tests import copy_file_to_tmp_path, expected_scaffold_set_values


def test_scaffolder_instantiates_as_type_scaffolder():
    # Instantiate Context object
    ctx = Context()

    # Instantiate scaffolder object
    scaff = Scaffolder(ctx)

    # Assert scaffolder object is of type Scaffolder
    assert isinstance(scaff, Scaffolder)


def test_apply_nodes_is_callable():
    # Instantiate Context object
    ctx = Context()

    # Instantiate scaffolder object
    scaff = Scaffolder(ctx)

    # Assert scaffolder object is of type Scaffolder
    assert callable(scaff.apply_nodes)


def test_create_is_callable():
    # Instantiate Context object
    ctx = Context()

    # Instantiate scaffolder object
    scaff = Scaffolder(ctx)

    # Assert scaffolder object is of type Scaffolder
    assert callable(scaff.create)


def test_context_initializes_correctly():
    # Instantiate Context object
    ctx = Context()

    # Instantiate scaffolder object
    scaff = Scaffolder(ctx)

    # Assert Scaffolder.context is initialized
    assert isinstance(scaff.context, Context)


def test_load_is_callable():
    # Instantiate Context object
    ctx = Context()

    # Instantiate scaffolder object
    scaff = Scaffolder(ctx)

    # Assert Scaffolder.load is callable
    assert callable(scaff.load)


def test_load_loads_registry_meta_data_into_memory(
    monkeypatch: MonkeyPatch, tmp_path: Path
):
    # Instantiate Context object
    ctx = Context()

    # Get .test_data/test_registry.toml filepath before patching to tmp_path
    registry_file = "test_registry.toml"
    source = ctx.test_dir / ".test_data" / registry_file
    destination = tmp_path / registry_file

    copy_file_to_tmp_path(monkeypatch, tmp_path=destination, source=source)

    # Instantiate scaffolder object
    scaff = Scaffolder(ctx, registry_path=destination)

    # Expected load data values
    set_name = "test_set"
    expected_data: dict[str, str | list[Node]] = {
        "set_name": set_name,
        "version": "0.0.1",
        "description": "Test scaffold.",
    }

    # Load test scaffold from test_registry.toml
    scaff.load(set_name)

    # Assert meta data is not None
    assert scaff.selected_set["set_name"] is not None
    assert scaff.selected_set["version"] is not None
    assert scaff.selected_set["description"] is not None

    # Assert meta data loads into memory
    assert scaff.selected_set["set_name"] == expected_data["set_name"]
    assert scaff.selected_set["version"] == expected_data["version"]
    assert scaff.selected_set["description"] == expected_data["description"]


def test_load_loads_nodes_list_into_memory(monkeypatch: MonkeyPatch, tmp_path: Path):
    # Instantiate Context object
    ctx = Context()

    # Get .test_data/test_registry.toml filepath before patching to tmp_path
    registry_file = "test_registry.toml"
    source = ctx.test_dir / ".test_data" / registry_file
    destination = tmp_path / registry_file

    copy_file_to_tmp_path(monkeypatch, tmp_path=destination, source=source)

    # Instantiate scaffolder object
    scaff = Scaffolder(ctx, registry_path=destination)

    # Expected load data values
    set_name = "test_set"
    expected_data: list[Node] = [
        Node(
            type="file",
            path=Path(".lichen/registry.toml"),
            template=Path("test/path/.lichen/registry.toml"),
        ),
        Node(
            type="file",
            path=Path(".gitignore"),
            template=Path("test/path/.gitignore"),
        ),
    ]

    # Load test scaffold from test_registry.toml
    scaff.load(set_name)

    # Assert selected_set is not None
    assert scaff.selected_set is not None

    # Assert nodes loads into memory
    nodes = scaff.selected_set["nodes"]
    assert nodes is not None

    for i, node in enumerate(nodes):
        assert node["type"] == expected_data[i].type
        assert node["path"] == expected_data[i].path
        assert node["template"] == expected_data[i].template


def test_save_is_callable():
    # Instantiate Context object
    ctx = Context()

    # Instantiate scaffolder object
    scaff = Scaffolder(ctx)

    # Assert Scaffolder.save is callable
    assert callable(scaff.save)


def test_save_saves_scaffold_data_to_registry(monkeypatch: MonkeyPatch, tmp_path: Path):
    # Instantiate Context object
    ctx = Context()

    # Get .test_data/test_registry.toml filepath before patching to tmp_path
    registry_file = "test_registry.toml"
    registry_path = ctx.test_dir / ".test_data" / registry_file
    destination = tmp_path / registry_file

    # Copy registry file to tmp_path
    copy_file_to_tmp_path(monkeypatch, tmp_path=destination, source=registry_path)

    scaff = Scaffolder(ctx, registry_path=destination)

    expected = expected_scaffold_set_values(version="0.0.2")

    # Save the current scaffold to the registry
    scaff.save(expected)

    # Get updated registry data to test save wrote properly
    updated = scaff.registry.load(destination, expected["set_name"])

    # Assert updated meta data is equivalent to expected meta data values
    assert updated["set_name"] == expected["set_name"]
    assert updated["version"] == expected["version"]
    assert updated["description"] == expected["description"]

    # Assert updated nodes are equivalent to expected nodes values
    for i, node in enumerate(updated["nodes"]):
        assert node.type == expected["nodes"][i].type
        assert node.path == expected["nodes"][i].path
        assert node.template == expected["nodes"][i].template
