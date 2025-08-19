from pytest import raises

from core.registry import Registry
from core.utils.tests import registry_arguments


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
