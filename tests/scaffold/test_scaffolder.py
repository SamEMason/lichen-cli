from pathlib import Path

from core.context import Context
from core.scaffold import Node, Scaffolder


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


def test_load_loads_meta_data_from_template():
    # Instantiate Context object
    ctx = Context()

    # Instantiate scaffolder object
    scaff = Scaffolder(ctx)

    # Expected load data values
    expected_data: dict[str, str | list[Node]] = {
        "set_name": "test",
        "version": "0.0.1",
        "description": "Test scaffold.",
    }

    # Load test scaffold from test_registry.toml
    path = ctx.test_dir / ".test_data" / "test_registry.toml"
    scaff.load(path)

    # Assert meta data is not None
    assert scaff.meta is not None

    # Assert meta data loads into memory
    assert scaff.meta.get("set_name") == expected_data["set_name"]
    assert scaff.meta.get("version") == expected_data["version"]
    assert scaff.meta.get("description") == expected_data["description"]


def test_load_loads_nodes_from_template():
    # Instantiate Context object
    ctx = Context()

    # Instantiate scaffolder object
    scaff = Scaffolder(ctx)

    # Expected load data values
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
    path = ctx.test_dir / ".test_data" / "test_registry.toml"
    scaff.load(path)

    # Assert meta data is not None
    assert scaff.scaffold is not None

    # Assert meta data loads into memory
    nodes = scaff.scaffold

    # Assert nodes loads into memory
    assert nodes is not None

    for i, node in enumerate(nodes):
        assert node["type"] == expected_data[i].type


def test_save_is_callable():
    # Instantiate Context object
    ctx = Context()

    # Instantiate scaffolder object
    scaff = Scaffolder(ctx)

    # Assert Scaffolder.save is callable
    assert callable(scaff.save)
