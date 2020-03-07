import pytest

from pyvavr import ValueException
from pyvavr.either import Either, Right, Left


def test_left_creation():
    either = Left("Some")

    assert either != None
    assert either.is_left() == True
    assert either.is_right() == False
    assert either.left == "Some"


def test_right_creation():
    either = Right("Some")

    assert either != None
    assert either.is_left() == False
    assert either.is_right() == True
    assert either.right == "Some"


def test_map_on_right_either_applies_function():
    either = Right("Some").map(lambda x: x + " More")

    assert either != None
    assert either.is_left() == False
    assert either.is_right() == True
    assert either.right == "Some More"


def test_map_on_left_either_does_nothing():
    either = Left("Some").map(lambda x: x + " More")

    assert either != None
    assert either.is_left() == True
    assert either.is_right() == False
    assert either.left == "Some"


def test_map_left_on_right_either_does_nothing():
    either = Right("Some").map_left(lambda x: x + " More")

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
