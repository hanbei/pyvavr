from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Callable

LEFT = TypeVar("LEFT")
RIGHT = TypeVar("RIGHT")
U = TypeVar("U")


class Either(ABC, Generic[LEFT, RIGHT]):

    def __init__(self):
        super().__init__()
        self._left = None
        self._right = None

    @abstractmethod
    def is_left(self):
        pass

    @abstractmethod
    def is_right(self):
        pass

    def map(self, function: Callable[[RIGHT], U]) -> 'Either[LEFT, U]':
        if (self.is_right()):
            return Right(function(self._right))
        else:
            return self

    def map_left(self, function: Callable[[LEFT], U]) -> 'Either[U, RIGHT]':
        if (self.is_left()):
            return Left(function(self._left))
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


class Right(Either):

    def __init__(self, right: RIGHT):
        super().__init__()
        self._right = right

    def is_right(self):
        return True

    def is_left(self):
        return False
