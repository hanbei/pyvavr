from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Callable, Tuple

from pyvavr import ValueException

T = TypeVar("T")  # pragma: no mutate
U = TypeVar("U")  # pragma: no mutate
R = TypeVar("R")  # pragma: no mutate


class ImmutableList(ABC, Generic[T]):

    @staticmethod
    def of(*values: T) -> 'ImmutableList[T]':
        result = Nil()
        for value in reversed(values):
            result = result.prepend(value)
        return result

    @staticmethod
    def range(start: int, end: int, step: int = 1):
        list = ImmutableList.of()
        sign = _sign(step)
        for x in range(end - sign, start - sign, -step):
            list = list.prepend(x)
        return list

    @staticmethod
    def of_list(list: List[T]) -> 'ImmutableList[T]':
        result = Nil()
        for value in reversed(list):
            result = result.prepend(value)
        return result

    @staticmethod
    def empty():
        return Nil()

    @abstractmethod
    def __len__(self):
        pass

    def __iter__(self):
        return ImmutableListIterator(self)

    @abstractmethod
    def head(self) -> T:
        pass

    @abstractmethod
    def tail(self) -> 'ImmutableList[T]':
        pass

    @abstractmethod
    def map(self, func: Callable[[T], U]) -> 'ImmutableList[U]':
        pass

    @abstractmethod
    def reverse(self) -> 'ImmutableList[T]':
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        pass

    @abstractmethod
    def fold_left(self, zero: U, combine: Callable[[U, T], U]) -> U:
        pass

    def prepend(self, value: T) -> 'ImmutableList[T]':
        return Cons(value, self)

    def peek(self) -> T:
        return self.head()

    def pop(self) -> 'ImmutableList[T]':
        return self.tail()

    def push(self, value: T) -> 'ImmutableList[T]':
        return self.prepend(value)

    def drop(self, n: int) -> 'ImmutableList[T]':
        if n <= 0:
            return self

        if n >= len(self):
            return ImmutableList.empty()

        result = self
        for i in range(0, n):
            if result.is_empty():
                return result

            result = result.tail()

        return result

    def drop_right(self, n: int) -> 'ImmutableList[T]':
        return self.reverse().drop(n).reverse()

    def drop_until(self, predicate: Callable[[T], bool]) -> 'ImmutableList[T]':
        return self.drop_while(lambda x: not predicate(x))

    def drop_right_until(self, predicate: Callable[[T], bool]) -> 'ImmutableList[T]':
        return self.drop_right_while(lambda x: not predicate(x))

    def drop_while(self, predicate: Callable[[T], bool]) -> 'ImmutableList[T]':
        result = self
        while not result.is_empty() and predicate(result.head()):
            result = result.tail()

        return result

    def drop_right_while(self, predicate: Callable[[T], bool]) -> 'ImmutableList[T]':
        return self.reverse().drop_while(predicate).reverse()

    @abstractmethod
    def or_else(self, list: 'ImmutableList[U]') -> 'ImmutableList[U]':
        pass

    def take(self, n: int) -> 'ImmutableList[T]':
        if n <= 0:
            return ImmutableList.empty()

        if n >= len(self):
            return self

        result = ImmutableList.empty()
        current = self
        for i in range(0, n):
            if current.is_empty():
                return result
            result = result.prepend(current.head())

            current = current.tail()

        return result.reverse()

    def take_until(self, predicate: Callable[[T], bool]) -> 'ImmutableList[T]':
        result = ImmutableList.empty()
        current = self
        while not current.is_empty() and not predicate(current.head()):
            result = result.prepend(current.head())
            current = current.tail()

        return result.reverse()

    def take_while(self, predicate: Callable[[T], bool]) -> 'ImmutableList[T]':
        return self.take_until(lambda x: not predicate(x))

    def take_right(self, n: int) -> 'ImmutableList[T]':
        return self.reverse().take(n).reverse()

    def take_right_until(self, predicate: Callable[[T], bool]) -> 'ImmutableList[T]':
        return self.reverse().take_until(predicate).reverse()

    def take_right_while(self, predicate: Callable[[T], bool]) -> 'ImmutableList[T]':
        return self.reverse().take_while(predicate).reverse()

    def filter(self, predicate: Callable[[T], bool]) -> 'ImmutableList[T]':
        result = ImmutableList.empty()
        current = self
        while not current.is_empty():
            if predicate(current.head()):
                result = result.prepend(current.head())
            current = current.tail()

        return result.reverse()

    def flat_map(self, func: Callable[[List[T]], U]) -> 'ImmutableList[U]':
        current = self
        list = ImmutableList.empty()
        while not current.is_empty():
            for value in func(current.head()):
                list = list.prepend(value)
            current = current.tail()

        return list.reverse()

    def zip(self, other: 'ImmutableList[U]') -> 'ImmutableList[Tuple[T,U]]':
        return self.zip_with(other, lambda x, y: (x, y))

    def zip_with(self, other: 'ImmutableList[U]', mapper: Callable[[T, U], R]) -> 'ImmutableList[R]':
        if len(self) != len(other):
            raise ValueException("not same length")

        result = ImmutableList.empty()
        other_iter = iter(other)
        self_iter = iter(self)
        while True:
            try:
                x = next(self_iter)
                y = next(other_iter)
                result = result.prepend(mapper(x, y))
            except StopIteration:
                break

        return result.reverse()


# @abstractmethod
# def append(self, value: T) -> 'ImmutableList[T]':
#     pass
#
#
# @abstractmethod
# def partition(self, predicate: Callable[[T], bool]) -> 'ImmutableList[U]':
#     pass
#
# @abstractmethod
# def insert(self, index: int, element: T) -> 'ImmutableList[U]':
#     pass


class Cons(ImmutableList, Generic[T]):

    def __init__(self, value: T, next: ImmutableList[T]):
        self.value = value
        self.next = next

    def __len__(self):
        current = self
        acc = 0
        while not current.is_empty():
            acc += 1
            current = current.tail()
        return acc

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Cons):
            return self.value == o.value and self.next == o.next
        else:
            return False

    def __repr__(self):
        return "(" + str(self.value) + ", " + str(self.next) + ")"

    def map(self, func: Callable[[T], U]) -> ImmutableList[U]:
        current = self
        list = ImmutableList.empty()
        while not current.is_empty():
            list = list.prepend(func(current.head()))
            current = current.tail()

        return list.reverse()

    def reverse(self) -> ImmutableList[T]:
        current = self
        result = Nil()
        while not current.is_empty():
            result = result.prepend(current.head())
            current = current.tail()
        return result

    def head(self) -> T:
        return self.value

    def tail(self) -> ImmutableList[T]:
        return self.next

    def is_empty(self) -> bool:
        return False

    def fold_left(self, zero: U, combine: Callable[[U, T], U]) -> U:
        current = self
        result = zero
        while not current.is_empty():
            result = combine(result, current.head())
            current = current.tail()
        return result

    def or_else(self, list: 'ImmutableList[U]') -> 'ImmutableList[U]':
        return self


class Nil(ImmutableList):
    pass

    def __len__(self):
        return 0

    def __eq__(self, other):
        return isinstance(other, Nil)

    def __repr__(self):
        return "Nil()"

    def map(self, func: Callable[[T], U]) -> ImmutableList[U]:
        return Nil()

    def reverse(self) -> ImmutableList[T]:
        return Nil()

    def head(self) -> T:
        raise ValueException("No head of an empty list")

    def tail(self) -> ImmutableList[T]:
        raise ValueException("No tail of an empty list")

    def is_empty(self) -> bool:
        return True

    def fold_left(self, zero: U, combine: Callable[[U, T], U]) -> U:
        return zero

    def or_else(self, list: 'ImmutableList[U]') -> 'ImmutableList[U]':
        return list


def _sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    elif x == 0:
        return 0
    else:
        return x


class ImmutableListIterator(Generic[T]):
    def __init__(self, immutable_list: ImmutableList[T]):
        self.immutable_list = immutable_list

    def __next__(self) -> T:
        if self.immutable_list.is_empty():
            raise StopIteration()

        current = self.immutable_list.head()
        self.immutable_list = self.immutable_list.tail()
        return current
