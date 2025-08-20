from pytest import raises

# from pytest import mark, raises

from core.context import Context
from core.registry import Registry, SelectedSet
from core.utils.tests import expected_registry_values, registry_arguments


def test_registry_instantiates_as_registry():
    # Initialize Registry arguments
    (path, selected_set) = registry_arguments()

    # Instantiate Context object
    registry = Registry(path, selected_set)

    # Assert the Registry object is of type Registry
    assert isinstance(registry, Registry)


def test_registry_initializes_with_correct_parameters():
    # Initialize Registry arguments
    (path, selected_set) = registry_arguments()

    # Instantiate Context object
    registry = Registry(path, selected_set)

    # Assert Registry.path is initialized with correct path
    assert registry.path == path

    # Assert Registry.selected_set is initialized with correct string
    assert registry.selected_set == selected_set


def test_load_is_callable():
    # Initialize Registry arguments
    (path, selected_set) = registry_arguments()

    # Instantiate Context object
    registry = Registry(path, selected_set)

    # Assert Registry.load is callable
    assert callable(registry.load)


def test_load_raises_exception_when_file_does_not_exist():
    # Initialize Registry arguments
    (path, selected_set) = registry_arguments(path="non_existent_file_path")

    # Instantiate Context object
    registry = Registry(path, selected_set)

    # Call load with non-existent file path
    with raises(FileNotFoundError):
        registry.load(path, selected_set)


def test_load_raises_exception_when_selected_set_does_not_exist():
    # Initialize Registry arguments
    (path, selected_set) = registry_arguments(selected_set="non_existent_set")

    # Instantiate Context object
    registry = Registry(path, selected_set)

    # Call load with non-existent file path
    with raises(KeyError):
        registry.load(path, selected_set)


def test_save_is_callable():
    # Initialize Registry arguments
    (path, selected_set) = registry_arguments()

    # Instantiate Context object
    registry = Registry(path, selected_set)

    # Assert Registry.save is callable
    assert callable(registry.save)


# @mark.skip()
def test_save_writes_meta_data_to_registry():
    # Instantiate Context object
    ctx = Context()

    # Expected values to be written to registry
    set_name = "test_set"

    expected_values: SelectedSet = expected_registry_values(set_name=set_name)

    registry_load_path = ctx.test_dir / ".test_data" / "test_registry.toml"
    registry_save_path = ctx.test_dir / ".test_data" / "test_registry_save.toml"

    # Initialize Registry arguments
    (path, selected_set) = registry_arguments(path=registry_load_path)

    # Instantiate Context object
    registry = Registry(path, selected_set)

    # Save expected values to the registry
    registry.save(filepath=registry_save_path, set=expected_values)

    # Load data from registry to check against expected values
    loaded_set = registry.load(filepath=registry_save_path, select_set=set_name)

    # Assert loaded_set meta data is equivalent to expected meta data values
    assert loaded_set["set_name"] == expected_values["set_name"]
    assert loaded_set["version"] == expected_values["version"]
    assert loaded_set["description"] == expected_values["description"]


def test_save_raises_value_error_when_set_name_is_empty_string():
    # Instantiate Context object
    ctx = Context()

    expected_values: SelectedSet = expected_registry_values(set_name="")

    registry_path = ctx.test_dir / ".test_data" / "test_registry.toml"

    # Initialize Registry arguments
    (path, selected_set) = registry_arguments(path=registry_path)

    # Instantiate Context object
    registry = Registry(path, selected_set)

    with raises(ValueError):
        # Save expected values to the registry
        registry.save(filepath=registry_path, set=expected_values)
