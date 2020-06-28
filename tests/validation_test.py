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
    assert valid.valid() is True


def test_valid_is_not_invalid(valid):
    assert valid.invalid() is False


def test_invalid_is_invalid(invalid):
    assert invalid.invalid() is True


def test_invalid_is_not_valid(invalid):
    assert invalid.valid() is False


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


def test_swap_invalid(invalid):
    swapped = invalid.swap()
    assert swapped.valid()
    assert swapped.get() == "Error"


def test_swap_valid(valid):
    swapped = valid.swap()
    assert swapped.invalid()
    assert swapped.get_error() == "Some"


def test_map_on_valid_applies_function(valid):
    validation = valid.map(lambda x: x + " More")

    assert validation
    assert validation.valid() is True
    assert validation.get() == "Some More"


def test_map_on_invalid_does_nothing(invalid):
    validation = invalid.map(lambda x: x + " More")

    assert validation
    assert validation.invalid() is True
    assert validation.get_error() == "Error"


def test_bimap_on_valid_applies_valid_function(valid):
    validation = valid.bimap(lambda x: x + " More", lambda x: x + " Error")

    assert validation
    assert validation.valid() is True
    assert validation.get() == "Some More"


def test_bimap_on_invalid_applies_invalid_function(invalid):
    validation = invalid.bimap(lambda x: x + " More", lambda x: x + " Error")

    assert validation
    assert validation.invalid() is True
    assert validation.get_error() == "Error Error"


def test_filter_invalid_is_somethig(invalid):
    filtered = invalid.filter(lambda x: x == "Some")

    assert filtered.is_empty() is False
    assert filtered.get() == invalid


def test_filter_valid_matches(valid):
    filtered = valid.filter(lambda x: x == "Some")

    assert filtered.is_present() is True
    assert filtered.get() == valid


def test_filter_valid_does_not_match(valid):
    filtered = valid.filter(lambda x: x == "Bla")

    assert filtered.is_present() is False


def test_valid_or_else_is_same(valid):
    or_else = valid.or_else(Valid("alternative"))

    assert or_else == valid


def test_invalid_or_else_is_alternative(invalid):
    or_else = invalid.or_else(Valid("alternative"))

    assert or_else == Valid("alternative")


def test_valid_or_else_is_same_callable(valid):
    or_else = valid.or_else(lambda: Valid("alternative"))

    assert or_else == valid


def test_invalid_or_else_is_alternative_callable(invalid):
    or_else = invalid.or_else(lambda: Valid("alternative"))

    assert or_else == Valid("alternative")


def test_fold_valid(valid):
    assert valid.fold(lambda x: x + "Some", lambda x: x + "Erro") == "SomeSome"


def test_fold_invalid(invalid):
    assert invalid.fold(lambda x: x + "Some", lambda x: x + "Erro") == "ErrorErro"


class TestValidation(object):
    def __init__(self, value1, value2):
        self.value1 = value1
        self.value2 = value2


def create_validation(value1, value2):
    return TestValidation(value1, value2)


def test_ap(valid):
    ap = valid.combine(Valid(1)).ap(create_validation)

    assert ap
    assert isinstance(ap.get(), TestValidation)
    assert ap.get().value1 == "Some"
    assert ap.get().value2 == 1
