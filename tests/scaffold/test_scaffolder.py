from pathlib import Path
from pytest import raises

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
    set_name = "test_set"
    expected_data: dict[str, str | list[Node]] = {
        "set_name": set_name,
        "version": "0.0.1",
        "description": "Test scaffold.",
    }

    # Load test scaffold from test_registry.toml
    path = ctx.test_dir / ".test_data" / "test_registry.toml"
    scaff.load(path, set_name)

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
    path = ctx.test_dir / ".test_data" / "test_registry.toml"
    scaff.load(path, set_name)

    # Assert meta data is not None
    assert scaff.nodes is not None

    # Assert meta data loads into memory
    nodes = scaff.nodes

    # Assert nodes loads into memory
    assert nodes is not None

    for i, node in enumerate(nodes):
        assert node["type"] == expected_data[i].type


def test_extract_data_is_callable():
    # Instantiate Context object
    ctx = Context()

    # Instantiate scaffolder object
    scaff = Scaffolder(ctx)

    # Assert Scaffolder.save is callable
    assert callable(scaff.extract_data)


def test_extract_data_raises_exception_when_selected_set_does_not_exist():
    # Instantiate Context object
    ctx = Context()

    # Instantiate scaffolder object
    scaff = Scaffolder(ctx)

    # Instatiate non-existent file path
    path = ctx.test_dir / ".test_data" / "test_registry.toml"
    selected_set = "non_existent_set"

    # Call extract_data with non-existent file path
    with raises(KeyError):
        scaff.extract_data(path, selected_set)


def test_extract_data_raises_exception_when_file_does_not_exist():
    # Instantiate Context object
    ctx = Context()

    # Instantiate scaffolder object
    scaff = Scaffolder(ctx)

    # Instatiate non-existent file path
    assert ctx.project_root is not None
    path = ctx.project_root / "non" / "existent" / "path"
    selected_set = "test"

    # Call extract_data with non-existent file path
    with raises(FileNotFoundError):
        scaff.extract_data(path, selected_set)


def test_save_is_callable():
    # Instantiate Context object
    ctx = Context()

    # Instantiate scaffolder object
    scaff = Scaffolder(ctx)

    # Assert Scaffolder.save is callable
    assert callable(scaff.save)
