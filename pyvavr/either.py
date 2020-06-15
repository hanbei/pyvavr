from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Callable

from pyvavr import ValueException

LEFT = TypeVar("LEFT")  # pragma: no mutate
RIGHT = TypeVar("RIGHT")  # pragma: no mutate
U = TypeVar("U")  # pragma: no mutate


class Either(ABC, Generic[LEFT, RIGHT]):

    def __init__(self):
        super().__init__()

    @abstractmethod  # pragma: no mutate
    def is_left(self):
        pass

    @abstractmethod  # pragma: no mutate
    def is_right(self):
        pass

    @abstractmethod  # pragma: no mutate
    def right(self) -> RIGHT:
        pass

    @abstractmethod  # pragma: no mutate
    def left(self) -> LEFT:
        pass

    def map(self, function: Callable[[RIGHT], U]) -> 'Either[LEFT, U]':
        if self.is_right():
            return Right(function(self.right))
        else:
            return self

    def flat_map(self, function: Callable[[RIGHT], 'Either[U]']) -> 'Either[LEFT, U]':
        if self.is_right():
            return function(self.right)
        else:
            return self

    def map_left(self, function: Callable[[LEFT], U]) -> 'Either[U, RIGHT]':
        if self.is_left():
            return Left(function(self.left))
        else:
            return self


class Left(Either):

    def __init__(self, left: LEFT):
        super().__init__()
        self._left = left

    def is_left(self):
        return True

    def is_right(self):
        return False

    @property
    def right(self) -> RIGHT:
        raise ValueException("Not a right value")

    @property
    def left(self) -> LEFT:
        return self._left


class Right(Either):

    def __init__(self, right: RIGHT):
        super().__init__()
        self._right = right

    def is_right(self):
        return True

    def is_left(self):
        return False

    @property
    def right(self) -> RIGHT:
        return self._right

    @property
    def left(self) -> LEFT:
        raise ValueException("Not a left value")
