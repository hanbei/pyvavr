import pytest

from pyvavr import curry, CantCurryVarArgException


def add(x, y, z):
    return x + y + z


def add_all(*args):
    return sum(args)


def test_curry_non_varargs():
    curried_add = curry(add)
    assert callable(curried_add(1))
    assert callable(curried_add(1)(1))
    assert curried_add(1)(1)(1) == 3


def test_curry_varargs_with_flag():
    curried_add = curry(add_all, allow_var_args=True)
    assert callable(curried_add(1))
    assert callable(curried_add(1)(1))
    assert callable(curried_add(1)(1)(1))
    assert curried_add(1)(1)(1)() == 3

def test_curry_varargs_without_flag_raises_exception():
    with pytest.raises(CantCurryVarArgException):
        curry(add_all)
