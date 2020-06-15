import pytest

from pyvavr import ValueException
from pyvavr.validation import Valid, Invalid


@pytest.fixture()
def valid():
    return Valid("Some")


@pytest.fixture()
def invalid():
    return Invalid("Error")


def test_valid_is_valid(valid):
    assert valid.valid() == True


def test_valid_is_not_invalid(valid):
    assert valid.invalid() == False


def test_invalid_is_invalid(invalid):
    assert invalid.invalid() == True


def test_invalid_is_not_valid(invalid):
    assert invalid.valid() == False


def test_valid_get_returns_value(valid):
    assert valid.get() == "Some"


def test_invalid_error_returns_value(invalid):
    assert invalid.get_error() == "Error"


def test_valid_get_error_raises(valid):
    with pytest.raises(ValueException):
        valid.get_error()


def test_invalid_get_raises(invalid):
    with pytest.raises(ValueException):
        invalid.get()
