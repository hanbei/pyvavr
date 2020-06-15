import pytest

from pyvavr import ValueException
from pyvavr.either import Right, Left

@pytest.fixture()
def right():
    return Right("Some")

@pytest.fixture()
def left():
    return Left("Some")


def test_left_creation(left):
    assert left != None
    assert left.is_left() == True
    assert left.is_right() == False
    assert left.left == "Some"


def test_right_creation(right):
    assert right != None
    assert right.is_left() == False
    assert right.is_right() == True
    assert right.right == "Some"


def test_map_on_right_either_applies_function(right):
    either = right.map(lambda x: x + " More")

    assert either != None
    assert either.is_left() == False
    assert either.is_right() == True
    assert either.right == "Some More"


def test_map_on_left_either_does_nothing(left):
    either = left.map(lambda x: x + " More")

    assert either != None
    assert either.is_left() == True
    assert either.is_right() == False
    assert either.left == "Some"

def test_flat_map_on_right_either_applies_function(right):
    either = right.flat_map(lambda x: Right(x + " More"))

    assert either != None
    assert either.is_left() == False
    assert either.is_right() == True
    assert either.right == "Some More"


def test_flat_map_on_left_either_does_nothing(left):
    either = left.flat_map(lambda x: Right(x + " More"))

    assert either != None
    assert either.is_left() == True
    assert either.is_right() == False
    assert either.left == "Some"


def test_map_left_on_right_either_does_nothing(right):
    either = right.map_left(lambda x: x + " More")

    assert either != None
    assert either.is_left() == False
    assert either.is_right() == True
    assert either.right == "Some"


def test_map_left_on_left_either_applies_function():
    either = Left("Some").map_left(lambda x: x + " More")

    assert either != None
    assert either.is_left() == True
    assert either.is_right() == False
    assert either.left == "Some More"


def test_left_get_on_right_raises():
    with pytest.raises(ValueException):
        var = Right("Some").left


def test_right_get_on_left_raises():
    with pytest.raises(ValueException):
        var = Left("Some").right
