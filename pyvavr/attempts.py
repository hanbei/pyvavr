from abc import abstractmethod, ABC
from typing import TypeVar, Generic, Callable, Union

from pyvavr import ValueException

R = TypeVar("R")
T = TypeVar("T")
E = TypeVar("E")


class Try(ABC, Generic[T, E]):

    def __init__(self, function: Callable[..., R], *args, **kwargs):
        try:
            self._result = function(args, kwargs)
        except Exception as e:
            self._exception = e

    @classmethod
    def success(cls, result):
        return Success(result)

    @classmethod
    def failure(cls, exception):
        return Failure(exception)

    @abstractmethod
    def map(self, function: Callable[[T], R]) -> 'Try[R]':
        pass

    @abstractmethod
    def flat_map(self, function: Callable[[T], 'Try[R]']) -> 'Try[R]':
        pass

    @abstractmethod
    def get(self) -> T:
        pass

    @abstractmethod
    def get_error(self) -> E:
        pass

    @abstractmethod
    def or_else(self, alternative: Union[T, Callable[[], T]]) -> T:
        pass

    @abstractmethod
    def or_else_raise(self, alternative: Union[T, Callable[[], Exception]]) -> T:
        pass

    @abstractmethod
    def is_success(self) -> bool:
        pass

    def is_failure(self) -> bool:
        return not self.is_success()


class Success(Try):

    def __init__(self, result):
        super().__init__(lambda x: result)
        self._result = result

    def is_success(self) -> bool:
        return True

    def get(self) -> T:
        return self._result

    def get_error(self) -> E:
        raise ValueException("cause not supported on success")

    def or_else(self, alternative: Union[T, Callable[[], T]]) -> T:
        return self._result

    def or_else_raise(self, alternative: Union[T, Callable[[], Exception]]) -> T:
        return self._result

    def map(self, function: Callable[[T], R]) -> 'Try[R]':
        try:
            return Success(function(self._result))
        except Exception as e:
            return Failure(e)

    def flat_map(self, function: Callable[[T], 'Try[R]']) -> 'Try[R]':
        try:
            return function(self._result)
        except Exception as e:
            return Failure(e)


class Failure(Try):

    def __init__(self, exception: Exception):
        super().__init__(lambda x: None)
        self._exception = exception

    def is_success(self) -> bool:
        return False

    def get(self) -> T:
        raise self._exception

    def get_error(self) -> E:
        return self._exception

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
