from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Callable

from pyvavr import ValueException
from pyvavr.option import Just, Nothing, Option

E = TypeVar("E")  # pragma: no mutate
F = TypeVar("F")  # pragma: no mutate
T = TypeVar("T")  # pragma: no mutate
U = TypeVar("U")  # pragma: no mutate


class Validation(ABC, Generic[E, T]):

    @abstractmethod
    def valid(self) -> bool:
        pass

    @abstractmethod
    def invalid(self) -> bool:
        pass

    @abstractmethod
    def get(self) -> T:
        pass

    @abstractmethod
    def get_error(self) -> E:
        pass

    def swap(self) -> 'Validation[T, E]':
        if self.invalid():
            return Valid(self.get_error())
        else:
            return Invalid(self.get())

    def map(self, function: Callable[[T], U]) -> 'Validation[E, U]':
        if self.invalid():
            return Invalid(self.get_error())
        else:
            value = self.get()
            return Valid(function(value))

    def bimap(self, valid_function: Callable[[T], U], invalid_function: Callable[[E], F]) -> 'Validation[F, U]':
        if self.invalid():
            return Invalid(invalid_function(self.get_error()))
        else:
            return Valid(valid_function(self.get()))

    def map_error(self, function: Callable[[E], F]) -> 'Validation[F, T]':
        if self.invalid():
            error = self.get_error()
            return Invalid(function(error))
        else:
            return Valid(self.get())

    def filter(self, predicate: Callable[[T], bool]) -> 'Option[Validation[E, T]]':
        if self.invalid() or predicate(self.get()):
            return Just(self)
        else:
            return Nothing()


class Valid(Validation):
    def __init__(self, value: T):
        self.value = value

    def valid(self) -> bool:
        return True

    def invalid(self) -> bool:
        return False

    def get(self) -> T:
        return self.value

    def get_error(self) -> E:
        raise ValueException("error of 'valid' Validation");


class Invalid(Validation):
    def __init__(self, error: E):
        self.error = error

    def valid(self) -> bool:
        return False

    def invalid(self) -> bool:
        return True

    def get(self) -> T:
        raise ValueException("get of 'invalid' Validation");

    def get_error(self) -> E:
        return self.error
