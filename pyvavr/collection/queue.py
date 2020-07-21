from typing import Generic, TypeVar, List, Callable

from pyvavr import NoSuchElementException
from pyvavr.collection.list import ImmutableList

T = TypeVar("T")  # pragma: no mutate
U = TypeVar("U")  # pragma: no mutate


class ImmutableQueue(Generic[T]):

    def __init__(self, front: ImmutableList[T], rear: ImmutableList[T]):
        if front.is_empty():
            self.front = rear.reverse()
            self.rear = front
        else:
            self.front = front
            self.rear = rear

    @staticmethod
    def of(*values: T) -> 'ImmutableQueue[T]':
        front = ImmutableList.of(*values)
        rear = ImmutableList.empty()
        return ImmutableQueue(front, rear)

    @staticmethod
    def of_list(list: List[T]) -> 'ImmutableQueue[T]':
        front = ImmutableList.of_list(list)
        rear = ImmutableList.empty()
        return ImmutableQueue(front, rear)

    @staticmethod
    def empty():
        return ImmutableQueue(ImmutableList.empty(), ImmutableList.empty())

    def __len__(self):
        return len(self.front) + len(self.rear)

    def __iter__(self):
        pass

    def __eq__(self, other):
        return self.front == other.front and self.rear == other.rear

    def __repr__(self):
        return self.front.__repr__() + self.rear.__repr__()

    def map(self, func: Callable[[T], U]) -> 'ImmutableQueue[U]':
        pass

    def is_empty(self) -> bool:
        return self.front.is_empty() and self.rear.is_empty()

    def fold_left(self, zero: U, combine: Callable[[U, T], U]) -> U:
        pass

    def or_else(self, list: 'ImmutableQueue[U]') -> 'ImmutableQueue[U]':
        pass

    def filter(self, predicate: Callable[[T], bool]) -> 'ImmutableQueue[T]':
        pass

    def flat_map(self, func: Callable[[List[T]], U]) -> 'ImmutableQueue[U]':
        pass

    def enqueue(self, value: T) -> 'ImmutableQueue[T]':
        return ImmutableQueue(self.front, self.rear.prepend(value))

    def dequeue(self) -> T:
        if self.is_empty():
            raise NoSuchElementException()
        else:
            return (self.head(), self.tail())

    def peek(self) -> T:
        return self.front.head()

    def head(self) -> T:
        if self.is_empty():
            raise NoSuchElementException("head of empty list")
        else:
            return self.front.head()

    def tail(self) -> 'ImmutableQueue[T]':
        if self.is_empty():
            raise NoSuchElementException("tail of empty list")
        else:
            return ImmutableQueue(self.front.tail(), self.rear)
