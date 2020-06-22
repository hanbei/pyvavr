from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Callable, Union

from pyvavr.exceptions import ValueException

U = TypeVar("U")  # pragma: no mutate
T = TypeVar("T")  # pragma: no mutate


class Option(ABC, Generic[T]):

    def __init__(self, value):
        super().__init__()
        self._value = value

    @property
    def value(self) -> T:
        return self.get()

    @abstractmethod  # pragma: no mutate
    def is_empty(self) -> bool:
        pass

    def is_present(self) -> bool:
        return not self.is_empty()

    @abstractmethod  # pragma: no mutate
    def map(self, function: Callable[[T], U]) -> 'Option[U]':
        pass

    @abstractmethod  # pragma: no mutate
    def flat_map(self, function: Callable[[T], 'Option[U]']) -> 'Option[U]':
        pass

    @abstractmethod  # pragma: no mutate
    def get(self) -> T:
        pass

    @abstractmethod  # pragma: no mutate
    def or_else(self, alternative: Union[T, Callable[[], T]]) -> T:
        pass

    @abstractmethod  # pragma: no mutate
    def or_else_raise(self, alternative: Union[T, Callable[[], Exception]]) -> T:
        pass

    def __repr__(self) -> str:
        return "Option(" + self._value + ")"


class Just(Option):

    def __init__(self, value):
        super().__init__(value)
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
        super().__init__(None)

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
