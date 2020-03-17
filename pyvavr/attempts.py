from abc import abstractmethod, ABC
from typing import TypeVar, Generic, Callable, Union

from pyvavr import ValueException

R = TypeVar("R")  # pragma: no mutate
T = TypeVar("T")  # pragma: no mutate
E = TypeVar("E")  # pragma: no mutate


class Try(ABC, Generic[T, E]):

    def __init__(self, value):
        super().__init__()
        self._value = value

    @classmethod  # pragma: no mutate
    def of(cls, function: Callable[..., R], *args, **kwargs):
        try:
            return Success(function(args, kwargs))
        except Exception as exception:
            return Failure(exception)

    @classmethod  # pragma: no mutate
    def success(cls, result):
        return Success(result)

    @classmethod  # pragma: no mutate
    def failure(cls, exception):
        return Failure(exception)

    @abstractmethod  # pragma: no mutate
    def map(self, function: Callable[[T], R]) -> 'Try[R]':
        pass

    @abstractmethod  # pragma: no mutate
    def flat_map(self, function: Callable[[T], 'Try[R]']) -> 'Try[R]':
        pass

    @abstractmethod  # pragma: no mutate
    def get(self) -> T:
        pass

    @abstractmethod  # pragma: no mutate
    def get_error(self) -> E:
        pass

    @abstractmethod  # pragma: no mutate
    def or_else(self, alternative: Union[T, Callable[[], T]]) -> T:
        pass

    @abstractmethod  # pragma: no mutate
    def or_else_raise(self, alternative: Union[T, Callable[[], Exception]]) -> T:
        pass

    @abstractmethod  # pragma: no mutate
    def is_success(self) -> bool:
        pass

    def is_failure(self) -> bool:
        return not self.is_success()

    def __repr__(self) -> str:
        return str(self._value)


class Success(Try):

    def __init__(self, value):
        super().__init__(value)
        # self._value = value

    def is_success(self) -> bool:
        return True

    def get(self) -> T:
        return self._value

    def get_error(self) -> E:
        raise ValueException("cause not supported on success")

    def or_else(self, alternative: Union[T, Callable[[], T]]) -> T:
        return self._value

    def or_else_raise(self, alternative: Union[T, Callable[[], Exception]]) -> T:
        return self._value

    def map(self, function: Callable[[T], R]) -> 'Try[R]':
        try:
            return Success(function(self._value))
        except Exception as e:
            return Failure(e)

    def flat_map(self, function: Callable[[T], 'Try[R]']) -> 'Try[R]':
        try:
            return function(self._value)
        except Exception as e:
            return Failure(e)


class Failure(Try):

    def __init__(self, exception: Exception):
        super().__init__(exception)

    def is_success(self) -> bool:
        return False

    def get(self) -> T:
        raise self._value

    def get_error(self) -> E:
        return self._value

    def map(self, function: Callable[[T], R]) -> 'Try[R]':
        return self

    def flat_map(self, function: Callable[[T], 'Try[R]']) -> 'Try[R]':
        return self

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
