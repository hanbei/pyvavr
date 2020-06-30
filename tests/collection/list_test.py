import pytest

from pyvavr import ValueException
from pyvavr.collection.list import Nil, Cons, ImmutableList


def test_nil_is_empty():
    assert len(Nil()) == 0
    assert Nil().is_empty() == True


def test_cons_is_not_empty():
    assert len(Cons(1, Nil())) == 1
    assert Cons(1, Nil()).is_empty() == False


def test_empty_prepend():
    assert Nil().prepend(1) == Cons(1, Nil())


def test_non_empty_prepend():
    assert Cons(2, Cons(3, Nil)).prepend(1) == Cons(1, Cons(2, Cons(3, Nil)))


def test_list_of():
    assert ImmutableList.of(1, 2, 3) == Cons(1, Cons(2, Cons(3, Nil())))


def test_reverse():
    assert ImmutableList.of(1, 2, 3).reverse() == Cons(3, Cons(2, Cons(1, Nil())))


def test_map():
    assert ImmutableList.of(1, 2, 3).map(lambda x: x + 2) == Cons(3, Cons(4, Cons(5, Nil())))


def test_list_range():
    assert ImmutableList.range(0, 5, 1) == Cons(0, Cons(1, Cons(2, Cons(3, Cons(4, Nil())))))


def test_list_range_reversed():
    assert ImmutableList.range(5, 0, -1) == Cons(5, Cons(4, Cons(3, Cons(2, Cons(1, Nil())))))


def test_recusrion_limit():
    list = ImmutableList.of(*[i for i in range(0, 2000)])
    assert len(list) == 2000


def test_head_nil_raises():
    with pytest.raises(ValueException):
        Nil().head()


def test_tail_nil_raises():
    with pytest.raises(ValueException):
        Nil().tail()


def test_head_cons_returns_first_element():
    assert Cons(1, Cons(2, Nil())).head() == 1


def test_tail_cons_returns_all_but_first():
    assert Cons(1, Cons(2, Nil())).tail() == Cons(2, Nil())
