from pathlib import Path
from pytest import MonkeyPatch, raises

from core.context import Context
from core.registry import Registry, ScaffoldSet
from core.utils.tests import (
    copy_file_to_tmp_path,
    expected_scaffold_set_values,
    registry_arguments,
)


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


def test_save_writes_updated_data_to_registry(monkeypatch: MonkeyPatch, tmp_path: Path):
    # Instantiate Context object
    ctx = Context()

    # Get .test_data/test_registry.toml filepath before patching to tmp_path
    registry_file = "test_registry.toml"
    source = ctx.test_dir / ".test_data" / registry_file
    destination = tmp_path / registry_file

    copy_file_to_tmp_path(monkeypatch, tmp_path=destination, source=source)

    # Expected values to be written to registry
    set_name = "test_set"
    expected: ScaffoldSet = expected_scaffold_set_values(
        set_name=set_name, version="0.0.2", nodes=[]
    )

    # File path to the registry file
    registry_path = tmp_path / registry_file

    # Initialize Registry arguments
    (path, selected_set) = registry_arguments(path=registry_path)

    # Instantiate Context object
    registry = Registry(path, selected_set)

    # Save expected values to the registry
    registry.save(registry_path=registry_path, set=expected)

    # Load data from registry to check against expected values
    updated = registry.load(filepath=registry_path, select_set=set_name)

    # Assert updated meta data is equivalent to expected meta data values
    assert updated["set_name"] == expected["set_name"]
    assert updated["version"] == expected["version"]
    assert updated["description"] == expected["description"]

    # Assert updated nodes are equivalent to expected nodes values
    assert updated["nodes"] == expected["nodes"]


def test_save_raises_value_error_when_set_name_is_empty_string():
    # Instantiate Context object
    ctx = Context()

    expected_values: ScaffoldSet = expected_scaffold_set_values(set_name="")

    registry_path = ctx.test_dir / ".test_data" / "test_registry.toml"

    # Initialize Registry arguments
    (path, selected_set) = registry_arguments(path=registry_path)

    # Instantiate Context object
    registry = Registry(path, selected_set)

    with raises(ValueError):
        # Save expected values to the registry
        registry.save(registry_path=registry_path, set=expected_values)


def test_save_raises_key_error_when_set_name_is_not_valid_key():
    # Instantiate Context object
    ctx = Context()

    expected_values: ScaffoldSet = expected_scaffold_set_values(set_name="bad_key")

    registry_path = ctx.test_dir / ".test_data" / "test_registry.toml"

    # Initialize Registry arguments
    (path, selected_set) = registry_arguments(path=registry_path)

    # Instantiate Context object
    registry = Registry(path, selected_set)

    with raises(KeyError):
        # Save expected values to the registry
        registry.save(registry_path=registry_path, set=expected_values)
