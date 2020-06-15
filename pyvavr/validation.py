from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Callable, Union

U = TypeVar("U")  # pragma: no mutate
T = TypeVar("T")  # pragma: no mutate


class Validation(ABC, Generic[U,T]):
    pass