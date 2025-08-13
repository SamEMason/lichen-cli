from core.scaffold import Scaffolder


def test_scaffolder_instantiates_as_type_scaffolder():
    # Instantiate scaffolder object
    scaff = Scaffolder()

    # Assert scaffolder object is of type Scaffolder
    assert isinstance(scaff, Scaffolder)
