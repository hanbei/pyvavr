from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Callable, Union

from pyvavr import ValueException

U = TypeVar("U")
T = TypeVar("T")


class Option(ABC, Generic[T]):

    def __init__(self):
        super().__init__()
        self._value = None

    @property
    def value(self) -> T:
        return self.get()

    @abstractmethod
    def is_empty(self) -> bool:
        pass

    def is_present(self) -> bool:
        return not self.is_empty()

    @abstractmethod
    def map(self, function: Callable[[T], U]) -> 'Option[U]':
        pass

    @abstractmethod
    def flat_map(self, function: Callable[[T], 'Option[U]']) -> 'Option[U]':
        pass

    @abstractmethod
    def get(self) -> T:
        pass

    @abstractmethod
    def or_else(self, alternative: Union[T, Callable[[], T]]) -> T:
        pass

    @abstractmethod
    def or_else_raise(self, alternative: Union[T, Callable[[], Exception]]) -> T:
        pass

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

    def or_else(self, alternative: Union[T, Callable[[], T]]) -> T:
        return self._value

    def or_else_raise(self, alternative: Union[T, Callable[[], Exception]]) -> T:
        return self._value

    def map(self, function: Callable[[T], U]) -> 'Option[U]':
        return Just(function(self._value))

    def flat_map(self, function: Callable[[T], 'Option[U]']) -> 'Option[U]':
        return function(self._value)


class Nothing(Option):

    def __init__(self):
        super().__init__()
        self._value = None

    def is_empty(self):
        return True

    def get(self) -> T:
        raise ValueException()

    def or_else(self, alternative: Union[T, Callable[[], T]]) -> T:
        if callable(alternative):
            return alternative()
        else:
            return alternative

    def or_else_raise(self, alternative: Union[T, Callable[[], Exception]]) -> T:
        if callable(alternative):
            raise alternative()
        else:
            raise alternative

    def map(self, function: Callable[[T], U]) -> 'Option[U]':
        return self

    def flat_map(self, function: Callable[[T], 'Option[U]']) -> 'Option[U]':
        return self

