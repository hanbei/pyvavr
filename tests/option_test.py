import pytest

from pyvavr import ValueException
from pyvavr.option import Just, Nothing


def test_empty_option():
    option = Nothing()

    assert option.is_empty() == True
    assert option.is_present() == False


def test_just_option():
    option = Just("Some")

    assert option.is_empty() == False
    assert option.is_present() == True


def test_just_with_none_raises():
    with pytest.raises(ValueException):
        Just(None)


def test_map_on_just_applies_function():
    option = Just("Some").map(lambda x: x + " More")

    assert option
    assert option.is_empty() == False
    assert option.is_present() == True
    assert option._value == "Some More"


def test_map_on_empty_does_nothing():
    option = Nothing().map(lambda x: x + " More")

    assert option != None
    assert option.is_empty() == True
    assert option.is_present() == False

def test_flat_map_on_just_applies_function():
    option = Just("Some").flat_map(lambda x: Just(x + " More"))

    assert option
    assert option.is_empty() == False
    assert option.is_present() == True
    assert option._value == "Some More"


def test_flat_map_on_empty_does_nothing():
    option = Nothing().flat_map(lambda x: Just(x + " More"))

    assert option != None
    assert option.is_empty() == True
    assert option.is_present() == False



def test_get_on_just_returns_value():
    value = Just("Some").get()

    assert value == "Some"


def test_get_on_empty_raises_value_exception():
    with pytest.raises(ValueException):
        Nothing().get()


def test_nothing_or_else_with_value():
    assert Nothing().or_else("Alternative") == "Alternative"


def test_nothing_or_else_with_callable():
    assert Nothing().or_else(lambda: "Alternative2") == "Alternative2"

def test_just_or_else_with_value():
    assert Just("Some").or_else("Alternative") == "Some"


def test_just_or_else_with_callable():
    assert Just("Some").or_else(lambda: "Alternative2") == "Some"

def test_access_property():
    assert Just("Some").value == "Some"


def test_access_property_on_empty():
    with pytest.raises(ValueException):
        Nothing().value


def test_nothing_or_else_raise_with_value():
    with pytest.raises(ValueException):
        Nothing().or_else_raise(ValueException("Bäm"))


def test_nothing_or_else_raise_with_callable():
    with pytest.raises(ValueException):
        Nothing().or_else_raise(raise_something)

def test_just_or_else_raise_with_value():
    assert Just("Some").or_else_raise(ValueException("Bäm")) == "Some"


def test_just_or_else_raise_with_callable():
    assert Just("Some").or_else_raise(raise_something) == "Some"


def raise_something():
    raise ValueException("Something")