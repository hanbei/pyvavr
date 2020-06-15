import pytest

from pyvavr import ValueException
from pyvavr.option import Just, Nothing


@pytest.fixture()
def nothing():
    return Nothing()

@pytest.fixture()
def just():
    return Just("Some")


def test_empty_option(nothing):
    assert nothing.is_empty() == True
    assert nothing.is_present() == False


def test_just_option(just):
    assert just.is_empty() == False
    assert just.is_present() == True


def test_just_with_none_raises():
    with pytest.raises(ValueException):
        Just(None)


def test_map_on_just_applies_function(just):
    option = just.map(lambda x: x + " More")

    assert option
    assert option.is_empty() == False
    assert option.is_present() == True
    assert option._value == "Some More"


def test_map_on_empty_does_nothing(nothing):
    option = nothing.map(lambda x: x + " More")

    assert option != None
    assert option.is_empty() == True
    assert option.is_present() == False

def test_flat_map_on_just_applies_function(just):
    option = just.flat_map(lambda x: Just(x + " More"))

    assert option
    assert option.is_empty() == False
    assert option.is_present() == True
    assert option._value == "Some More"


def test_flat_map_on_empty_does_nothing(nothing):
    option = nothing.flat_map(lambda x: Just(x + " More"))

    assert option != None
    assert option.is_empty() == True
    assert option.is_present() == False



def test_get_on_just_returns_value(just):
    value = just.get()

    assert value == "Some"


def test_get_on_empty_raises_value_exception(nothing):
    with pytest.raises(ValueException):
        nothing.get()


def test_nothing_or_else_with_value(nothing):
    assert nothing.or_else("Alternative") == "Alternative"


def test_nothing_or_else_with_callable(nothing):
    assert nothing.or_else(lambda: "Alternative2") == "Alternative2"

def test_just_or_else_with_value(just):
    assert just.or_else("Alternative") == "Some"


def test_just_or_else_with_callable(just):
    assert just.or_else(lambda: "Alternative2") == "Some"

def test_access_property(just):
    assert just.value == "Some"


def test_access_property_on_empty(nothing):
    with pytest.raises(ValueException):
        nothing.value


def test_nothing_or_else_raise_with_value(nothing):
    with pytest.raises(ValueException):
        nothing.or_else_raise(ValueException("Bäm"))


def test_nothing_or_else_raise_with_callable(nothing):
    with pytest.raises(ValueException):
        nothing.or_else_raise(raise_something)

def test_just_or_else_raise_with_value(just):
    assert just.or_else_raise(ValueException("Bäm")) == "Some"


def test_just_or_else_raise_with_callable(just):
    assert just.or_else_raise(raise_something) == "Some"


def raise_something():
    raise ValueException("Something")