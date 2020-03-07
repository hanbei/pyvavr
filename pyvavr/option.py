from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Callable, Union

from pyvavr import ValueException

U = TypeVar("U")
T = TypeVar("T")


class Option(ABC, Generic[U]):

    def __init__(self):
        super().__init__()
        self._value = None

    @property
    def value(self):
        return self.get()

    @abstractmethod
    def is_empty(self):
        pass

    def is_present(self) -> bool:
        return not self.is_empty()

    def map(self, function: Callable[[U], T]) -> 'Option[T]':
        if (self.is_empty()):
            return self
        else:
            return Just(function(self._value))

    @abstractmethod
    def get(self) -> T:
        pass

    def or_else(self, alternative: Union[T, Callable[[], T]]) -> T:
        if self.is_empty():
            if callable(alternative):
                return alternative()
            else:
                return alternative
        else:
            return self.get()

    def __repr__(self) -> str:
        return "Option(" + self._value + ")"


class Just(Option):

    def __init__(self, value):
        super().__init__()
        if value:
            self._value = value
        else:
            raise ValueException("Just may not be None")

    def is_empty(self):
        return False

    def get(self) -> T:
        return self._value


class Nothing(Option):

    def __init__(self):
        super().__init__()
        self._value = None

    def is_empty(self):
        return True

    def get(self) -> T:
        raise ValueException()
