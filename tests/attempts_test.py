import pytest

from pyvavr import ValueException
from pyvavr.attempts import Try


@pytest.fixture
def failed_try():
    return Try.failure(Exception("Some error"))


@pytest.fixture
def successful_try():
    return Try.success("Some")


def test_failure_is_failure(failed_try):
    assert failed_try.is_failure() == True


def test_success_is_not_failure(successful_try):
    assert successful_try.is_failure() == False


def test_map_success(successful_try):
    assert successful_try.map(lambda x: x + " Bla").get() == "Some Bla"

def test_flat_map_success(successful_try):
    assert successful_try.flat_map(lambda x: Try.success(x + " Bla")).get() == "Some Bla"


def failing_map(x):
    raise NotImplementedError()


def test_map_fails_is_failure(successful_try):
    try_map = successful_try.map(failing_map)
    assert try_map.is_failure() == True
    assert isinstance(try_map.get_error(), NotImplementedError)


def test_map_failure(failed_try):
    try_map = failed_try.map(lambda x: x + " Bla")
    assert try_map.or_else("Test") == "Test"
    assert try_map.is_failure() == True


def test_flat_map_fails_is_failure(successful_try):
    try_map = successful_try.flat_map(failing_map)
    assert try_map.is_failure() == True
    assert isinstance(try_map.get_error(), NotImplementedError)


def test_flat_map_failure(failed_try):
    try_map = failed_try.flat_map(lambda x: Try.success(x + " Bla"))
    assert try_map.or_else("Test") == "Test"
    assert try_map.is_failure() == True


def test_get_on_success_returns_value(successful_try):
    assert successful_try.get() == "Some"


def test_get_on_failure_returns_value(failed_try):
    with pytest.raises(Exception):
        var = failed_try.get()


def test_get_error_on_failure(failed_try):
    error = failed_try.get_error()
    assert isinstance(error, Exception)


def test_get_error_on_success(successful_try):
    with pytest.raises(ValueException):
        var = successful_try.get_error()


def test_or_else_failed(failed_try):
    assert failed_try.or_else("Other") == "Other"


def test_or_else_success(successful_try):
    assert successful_try.or_else("Other") == "Some"


def test_or_else_raise_failed(failed_try):
    with pytest.raises(ValueException):
        failed_try.or_else_raise(ValueException())


def test_or_else_raise_success(successful_try):
    assert successful_try.or_else_raise("Other") == "Some"

def test_or_else_raise_failed_with_callable(failed_try):
    with pytest.raises(NotImplementedError):
        failed_try.or_else_raise(raise_something)


def test_or_else_raise_success_with_callable(successful_try):
    assert successful_try.or_else_raise(raise_something) == "Some"


def test_success_is_success(successful_try):
    assert successful_try.is_success() == True


def test_failure_is_not_success(failed_try):
    assert failed_try.is_success() == False

def raise_something():
    raise NotImplementedError