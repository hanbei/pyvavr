from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Callable, Union, List

from pyvavr import ValueException, curry
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

    @abstractmethod
    def or_else(self, alternative: Union['Validation[E, T]', Callable[[], 'Validation[E, T]']]) -> 'Validation[E, T]':
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

    def fold(self, ifValid: Callable[[T], U], ifInvalid: Callable[[E], U]) -> U:
        if self.valid():
            return ifValid(self.get())
        else:
            return ifInvalid(self.get_error())

    def ap(self, validation: 'Validation[List[E], Callable[[T], U]]'):
        if self.valid():
            if validation.valid():
                f = validation.get()
                u = f(self.get())
                return Valid(u)
            else:
                errors = validation.get_error()
                return Invalid(errors)
        else:
            if validation.valid():
                error = self.get_error()
                return Invalid([error])
            else:
                errors = validation.get_error()
                error = self.get_error()
                return Invalid(errors.append(error))

    def combine(self, v1: 'Validation[E, T]') -> 'ValidationBuilder':
        return ValidationBuilder(self, v1)


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
        raise ValueException("error of 'valid' Validation")

    def or_else(self, alternative: Union['Validation[E, T]', Callable[[], 'Validation[E, T]']]) -> 'Validation[E, T]':
        return self

    def __eq__(self, o: Validation[E, T]) -> bool:
        if o.invalid():
            return False
        else:
            return self.value == o.get()


class Invalid(Validation):
    def __init__(self, error: E) -> None:
        self.error = error

    def valid(self) -> bool:
        return False

    def invalid(self) -> bool:
        return True

    def get(self) -> T:
        raise ValueException("get of 'invalid' Validation");

    def get_error(self) -> E:
        return self.error

    def or_else(self, alternative: Union['Validation[E, T]', Callable[[], 'Validation[E, T]']]) -> 'Validation[E, T]':
        if callable(alternative):
            return alternative()
        else:
            return alternative

    def __eq__(self, o: Validation[E, T]) -> bool:
        if o.valid():
            return False
        else:
            return self.error == o.get_error()


class ValidationBuilder(Generic[E, T, U]):
    def __init__(self, *validations: Validation[E, T]) -> None:
        super().__init__()
        self.validations = list(validations)

    def combine(self, validation: Validation[E, T]):
        self.validations.append(validation)

    def ap(self, func: Callable):
        if len(self.validations) < 1:
            raise ValueException(message = "expected at least one validation")

        first_validation = self.validations[:][0]
        current_validation = first_validation.ap(Valid(curry(func)))

        for validation in self.validations[:][1:]:
            current_validation = validation.ap(current_validation)

        return current_validation


def combine(v1: Validation[E, T], v2: Validation[E, U]) -> ValidationBuilder:
    return ValidationBuilder(v1, v2)
