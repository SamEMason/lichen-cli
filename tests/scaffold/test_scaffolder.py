from core.context import Context
from core.scaffold import Scaffolder


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


def test_read_nodes_is_callable():
    # Instantiate Context object
    ctx = Context()

    # Instantiate scaffolder object
    scaff = Scaffolder(ctx)

    # Assert Scaffolder.read_nodes is callable
    assert callable(scaff.read_nodes)


def test_write_nodes_is_callable():
    # Instantiate Context object
    ctx = Context()

    # Instantiate scaffolder object
    scaff = Scaffolder(ctx)

    # Assert Scaffolder.write_nodes is callable
    assert callable(scaff.write_nodes)
