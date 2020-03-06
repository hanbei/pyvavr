from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Callable, Union

from pyvavr import ValueException

U = TypeVar("U")
T = TypeVar("T")


class Option(Generic[U]):

    @classmethod
    def of(cls, value: U) -> 'Option[U]':
        if (value == None):
            return Option(None)
        return Option(value)

    @classmethod
    def empty(cls) -> 'Option[U]':
        return Option(None)

    def __init__(self, value=None):
        super().__init__()
        self._value = value

    @property
    def value(self):
        return self.get()

    def is_empty(self):
        return self._value == None

    def is_present(self) -> bool:
        return not self.is_empty()

    def map(self, function: Callable[[U], T]) -> 'Option[T]':
        if (self.is_empty()):
            return self
        else:
            return Option.of(function(self._value))

    def get(self) -> T:
        if (self.is_empty()):
            raise ValueException()
        else:
            return self._value

    def or_else(self, alternative: Union[T, Callable[[], T]]) -> T:
        if self.is_empty():
            if callable(alternative):
                return alternative()
            else:
                return alternative
        else:
            return self.get()

    #    def __eq__(self, o: 'Option[T]') -> bool:
    #        return self._value == o._value

    def __repr__(self) -> str:
        return "Option(" + self._value + ")"
