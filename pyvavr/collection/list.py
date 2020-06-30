from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Callable

from pyvavr import ValueException

T = TypeVar("T")  # pragma: no mutate
U = TypeVar("U")  # pragma: no mutate


class ImmutableList(ABC, Generic[T]):

    @staticmethod
    def of(*values: List[T]) -> 'ImmutableList[T]':
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

    @abstractmethod
    def __len__(self):
        pass

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

    def prepend(self, value: T) -> 'ImmutableList[T]':
        return Cons(value, self)


class Cons(ImmutableList, Generic[T]):

    def __init__(self, value: T, next: ImmutableList[T]):
        self.value = value
        self.next = next

    def __len__(self):
        next = self
        acc = 0
        while next != Nil():
            acc += 1
            next = next.next
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
        list = Nil()
        while current != Nil():
            list = list.prepend(func(current.value))
            current = current.next

        return list.reverse()

    def reverse(self) -> ImmutableList[T]:
        current = self
        result = Nil()
        while current != Nil():
            result = result.prepend(current.value)
            current = current.next
        return result

    def head(self) -> T:
        return self.value

    def tail(self) -> ImmutableList[T]:
        return self.next

    def is_empty(self) -> bool:
        return False


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


def _sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    elif x == 0:
        return 0
    else:
        return x
