from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from pyvavr import ValueException

E = TypeVar("E")  # pragma: no mutate
T = TypeVar("T")  # pragma: no mutate


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
