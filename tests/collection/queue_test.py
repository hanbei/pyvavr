import pytest

from pyvavr import ValueException, NoSuchElementException
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
