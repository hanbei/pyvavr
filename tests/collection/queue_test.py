import pytest

from pyvavr import NoSuchElementException
from pyvavr.collection.list import ImmutableList
from pyvavr.collection.queue import ImmutableQueue


def test_of():
    queue = ImmutableQueue.of(1, 2, 3, 4, 5)
    assert queue == ImmutableQueue(ImmutableList.of(1, 2, 3, 4, 5), ImmutableList.empty())


def test_of_list():
    queue = ImmutableQueue.of_list([1, 2, 3, 4, 5])
    assert queue == ImmutableQueue(ImmutableList.of(1, 2, 3, 4, 5), ImmutableList.empty())


def test_enqueue():
    queue = ImmutableQueue.of(1, 2)

    queue = queue.enqueue(7)
    assert queue == ImmutableQueue(ImmutableList.of(1, 2), ImmutableList.of(7))

    queue = queue.enqueue(8)
    assert queue == ImmutableQueue(ImmutableList.of(1, 2), ImmutableList.of(8, 7))


def test_len():
    queue = ImmutableQueue.of(1, 2, 3, 4, 5, 6).enqueue(7)
    assert len(queue) == 7


def test_peek():
    queue = ImmutableQueue.empty().enqueue(7).enqueue(6).enqueue(4)
    assert queue.peek() == 7


def test_dequeue():
    queue = ImmutableQueue.empty().enqueue(7).enqueue(6).enqueue(4)
    assert queue.dequeue() == (7, ImmutableQueue.of(6, 4))


def test_dequeue_empty():
    queue = ImmutableQueue.empty()
    with pytest.raises(NoSuchElementException):
        queue.dequeue()


def test_head():
    queue = ImmutableQueue.empty().enqueue(7).enqueue(6).enqueue(4)
    assert queue.head() == 7


def test_head_empty():
    queue = ImmutableQueue.empty()
    with pytest.raises(NoSuchElementException):
        queue.head()


def test_tail():
    queue = ImmutableQueue.empty().enqueue(7).enqueue(6).enqueue(4)
    assert queue.tail() == ImmutableQueue.of(6, 4)


def test_tail_empty():
    queue = ImmutableQueue.empty()
    with pytest.raises(NoSuchElementException):
        queue.tail()


def test_map():
    queue = ImmutableQueue().enqueue(8).enqueue(6).enqueue(4).enqueue(2)
    queue = queue.map(lambda x: x + 2)
    assert queue == ImmutableQueue(ImmutableList.of(10), ImmutableList.of(4, 6, 8))


def test_flat_map():
    queue = ImmutableQueue().enqueue(3).enqueue(2).enqueue(1).enqueue(0)
    queue = queue.flat_map(lambda x: range(0, x))
    assert queue == ImmutableQueue(ImmutableList.of(0, 1, 2), ImmutableList.of(0, 0, 1))


def test_or_else_nil():
    assert ImmutableQueue.empty().or_else(ImmutableQueue.of(1, 2, 3, 4)) == ImmutableQueue.of(1, 2, 3, 4)


def test_or_else():
    assert ImmutableQueue.of(4, 5, 6).or_else(ImmutableQueue.of(1, 2, 3, 4)) == ImmutableQueue.of(4, 5, 6)


def test_fold_left():
    assert ImmutableQueue.range(1, 5).fold_left(0, lambda x, y: x + y) == 10
    assert ImmutableQueue.range(0, 2000).fold_left(0, lambda x, y: x + y) == 1999000


def test_filter():
    assert ImmutableQueue.of(1, 2, 3, 4, 5, 6).filter(lambda x: x % 2 == 0) == ImmutableQueue.of(2, 4, 6)


def test_filter_nil():
    assert ImmutableQueue.empty().filter(lambda x: x % 2 == 0) == ImmutableQueue.empty()
