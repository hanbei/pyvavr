import pytest
from pytest import fail

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


def test_list_of_list():
    assert ImmutableList.of_list([1, 2, 3]) == Cons(1, Cons(2, Cons(3, Nil())))


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


def test_fold_left():
    assert ImmutableList.range(1, 5).fold_left(0, lambda x, y: x + y) == 10
    assert ImmutableList.range(0, 2000).fold_left(0, lambda x, y: x + y) == 1999000


def test_iterator_nil():
    immutable_list = ImmutableList.empty()
    for i in immutable_list:
        fail("Should not reach statement")


def test_iterator():
    immutable_list = ImmutableList.of_list([1, 2, 3, 4, 5, 6])
    result = []
    for i in immutable_list:
        result.append(i)

    assert result == [1, 2, 3, 4, 5, 6]


def test_drop_nil():
    empty = ImmutableList.empty()
    assert empty.drop(1) == Nil()


def test_drop():
    list = ImmutableList.of(1, 2, 3, 4, 5, 6)
    assert list.drop(3) == ImmutableList.of(4, 5, 6)


def test_drop_less_than_zero():
    list = ImmutableList.of(1, 2, 3, 4, 5, 6)
    assert list.drop(-1) == list


def test_drop_more_than_len():
    list = ImmutableList.of(1, 2, 3, 4, 5, 6)
    assert list.drop(10) == ImmutableList.empty()


def test_drop_until():
    list = ImmutableList.of(1, 2, 3, 4, 5, 6)
    assert list.drop_until(lambda x: x > 3) == ImmutableList.of(4, 5, 6)


def test_drop_until_nil():
    list = ImmutableList.empty()
    assert list.drop_until(lambda x: x > 3) == ImmutableList.empty()


def test_drop_while():
    list = ImmutableList.of(1, 2, 3, 4, 5, 6)
    assert list.drop_while(lambda x: x < 3) == ImmutableList.of(3, 4, 5, 6)


def test_drop_while_nil():
    list = ImmutableList.empty()
    assert list.drop_while(lambda x: x < 3) == ImmutableList.empty()


def test_drop_right():
    list = ImmutableList.of(1, 2, 3, 4, 5, 6)
    assert list.drop_right(3) == ImmutableList.of(1, 2, 3)


def test_drop_right_less_than_zero():
    list = ImmutableList.of(1, 2, 3, 4, 5, 6)
    assert list.drop_right(-1) == list


def test_drop_right_more_than_len():
    list = ImmutableList.of(1, 2, 3, 4, 5, 6)
    assert list.drop_right(10) == ImmutableList.empty()


def test_drop_right_until():
    list = ImmutableList.of(1, 2, 3, 4, 5, 6)
    assert list.drop_right_until(lambda x: x <= 3) == ImmutableList.of(1, 2, 3)


def test_drop_right_until_nil():
    list = ImmutableList.empty()
    assert list.drop_right_until(lambda x: x < 3) == ImmutableList.empty()


def test_drop_right_while():
    list = ImmutableList.of(1, 2, 3, 4, 5, 6)
    assert list.drop_right_while(lambda x: x > 3) == ImmutableList.of(1, 2, 3)


def test_drop_right_while_nil():
    list = ImmutableList.empty()
    assert list.drop_right_while(lambda x: x > 3) == ImmutableList.empty()


def test_or_else_nil():
    assert ImmutableList.empty().or_else(ImmutableList.of(1, 2, 3, 4)) == ImmutableList.of(1, 2, 3, 4)


def test_or_else():
    assert ImmutableList.of(4, 5, 6).or_else(ImmutableList.of(1, 2, 3, 4)) == ImmutableList.of(4, 5, 6)
