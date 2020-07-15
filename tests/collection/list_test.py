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


def test_take_nil():
    assert ImmutableList.empty().take(2) == ImmutableList.empty()


def test_take():
    assert ImmutableList.of(1, 2, 3, 4, 5).take(3) == ImmutableList.of(1, 2, 3)


def test_take_less_than_zero():
    list = ImmutableList.of(1, 2, 3, 4, 5, 6)
    assert list.take(-1) == ImmutableList.empty()


def test_take_more_than_len():
    list = ImmutableList.of(1, 2, 3, 4, 5, 6)
    assert list.take(10) == list


def test_take_until():
    assert ImmutableList.of(1, 2, 3, 4, 5, 6).take_until(lambda x: x > 3) == ImmutableList.of(1, 2, 3)


def test_take_while():
    assert ImmutableList.of(1, 2, 3, 4, 5, 6).take_while(lambda x: x <= 3) == ImmutableList.of(1, 2, 3)


def test_take_right_nil():
    assert ImmutableList.empty().take_right(2) == ImmutableList.empty()


def test_take_right():
    assert ImmutableList.of(1, 2, 3, 4, 5).take_right(3) == ImmutableList.of(3, 4, 5)


def test_take__right_less_than_zero():
    list = ImmutableList.of(1, 2, 3, 4, 5, 6)
    assert list.take_right(-1) == ImmutableList.empty()


def test_take_right_more_than_len():
    list = ImmutableList.of(1, 2, 3, 4, 5, 6)
    assert list.take_right(10) == list


def test_take_right_until():
    assert ImmutableList.of(1, 2, 3, 4, 5, 6).take_right_until(lambda x: x < 3) == ImmutableList.of(3, 4, 5, 6)


def test_take_right_while():
    assert ImmutableList.of(1, 2, 3, 4, 5, 6).take_right_while(lambda x: x > 3) == ImmutableList.of(4, 5, 6)


def test_filter():
    assert ImmutableList.of(1, 2, 3, 4, 5, 6).filter(lambda x: x % 2 == 0) == ImmutableList.of(2, 4, 6)


def test_filter_nil():
    assert ImmutableList.empty().filter(lambda x: x % 2 == 0) == ImmutableList.empty()


def test_flat_map_nil():
    assert ImmutableList.empty().flat_map(lambda x: range(0, x)) == ImmutableList.empty()


def test_flat_map():
    assert ImmutableList.of(1, 2, 3).flat_map(lambda x: range(0, x)) == ImmutableList.of(0, 0, 1, 0, 1, 2)


def test_zip_with():
    list_one = ImmutableList.of(1, 2, 3, 4)
    list_two = ImmutableList.of(4, 3, 2, 1)
    assert list_one.zip_with(list_two, lambda x, y: x + y) == ImmutableList.of(5, 5, 5, 5)


def test_zip():
    list_one = ImmutableList.of(1, 2, 3, 4)
    list_two = ImmutableList.of(4, 3, 2, 1)
    assert list_one.zip(list_two) == ImmutableList.of((1, 4), (2, 3), (3, 2), (4, 1))
