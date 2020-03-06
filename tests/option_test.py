import pytest

from pyvavr import ValueException
from pyvavr.option import Option


def test_empty_option():
    option = Option.empty()

    assert option.is_empty() == True
    assert option.is_present() == False


def test_some_option():
    option = Option.of("Some")

    assert option.is_empty() == False
    assert option.is_present() == True


def test_some_with_none_is_empty():
    option = Option.of(None)

    assert option.is_empty() == True
    assert option.is_present() == False


def test_map_on_some_applies_function():
    option = Option.of("Some").map(lambda x: x + " More")

    assert option
    assert option.is_empty() == False
    assert option.is_present() == True
    assert option._value == "Some More"


def test_map_on_empty_does_nothing():
    option = Option.empty().map(lambda x: x + " More")

    assert option != None
    assert option.is_empty() == True
    assert option.is_present() == False


def test_map_on_empty_some_does_nothing():
    option = Option.of(None).map(lambda x: x + " More")

    assert option != None
    assert option.is_empty() == True
    assert option.is_present() == False
    assert option._value == None


def test_get_on_some_returns_value():
    value = Option.of("Some").get()

    assert value == "Some"


def test_get_on_empty_raises_value_exception():
    with pytest.raises(ValueException):
        Option.empty().get()


def test_get_on_none_some_raises_value_exception():
    with pytest.raises(ValueException):
        Option.of(None).get()


def test_or_else_with_value():
    assert Option.empty().or_else("Alternative") == "Alternative"


def test_or_else_with_callable():
    assert Option.empty().or_else(lambda: "Alternative2") == "Alternative2"


def test_or_else_with_value_none_some():
    assert Option.of(None).or_else("Alternative") == "Alternative"


def test_or_else_with_callable_none_some():
    assert Option.of(None).or_else(lambda: "Alternative") == "Alternative"


def test_access_property():
    assert Option.of("Some").value == "Some"

def test_access_property_on_empty():
    with pytest.raises(ValueException):
        var = Option.empty().value
