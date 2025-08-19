from core.context import Context
from core.registry import Registry


def test_registry_instantiates_as_registry():
    ctx = Context()

    # Instatiate registry file path and selected set
    path = ctx.test_dir / ".test_data" / "test_registry.toml"
    selected_set = "test_set"

    # Instantiate Context object
    registry = Registry(path, selected_set)

    # Assert the Registry object is of type Registry
    assert isinstance(registry, Registry)


def test_registry_initializes_with_correct_parameters():
    ctx = Context()

    # Instatiate registry file path and selected set
    path = ctx.test_dir / ".test_data" / "test_registry.toml"
    selected_set = "test_set"

    # Instantiate Context object
    registry = Registry(path, selected_set)

    # Assert Registry.path is initialized with correct path
    assert registry.path == path
    
    # Assert Registry.selected_set is initialized with correct string
    assert registry.selected_set == selected_set